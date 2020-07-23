from flask import (
    Flask, render_template, request)
from lib.TwitterListener import TweetsListener
from lib.Streaming import Streaming
import configparser
import tweepy as tw
import pandas as pd
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
import nltk
nltk.download('punkt')

app = Flask(__name__)

# Setup config
config_ini = configparser.ConfigParser()
config_ini.read('config/twitter.txt', encoding='utf-8')
API_KEY = config_ini['TWITTER']['API_KEY']
API_SECRET_KEY = config_ini['TWITTER']['API_SECRET_KEY']
ACCESS_TOKEN = config_ini['TWITTER']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config_ini['TWITTER']['ACCESS_TOKEN_SECRET']
FINBERT_MODEL_PATH = "models/sentiment/fin_phrasebank"

# CSV files
EXPORT_CSV_PATH = "output.csv"  # Where we store tweets collected
# CSV where we store result with predicted scores.
RESULT_CSV_PATH = "output.csv"

# Number of followers that we will use to verify if a tweet is trustable.
FOLLOWERS_THRESHOLD = 1000

# Twitter authentications
auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

# Declare classes we will be using
model = BertForSequenceClassification.from_pretrained(
    FINBERT_MODEL_PATH, num_labels=3, cache_dir=None)
listener = TweetsListener(EXPORT_CSV_PATH, FOLLOWERS_THRESHOLD, model)
stream = Streaming(auth, listener)


@ app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        df = pd.read_csv(RESULT_CSV_PATH)
        tags = listener.get_tags()  # Hashtags that user entered.
        return render_template('index.html',
                               tables=[df.to_html(classes='data table',
                                                  header="true")],
                               reload_status=True,
                               tags=tags)
    else:
        tags = {}  # Used to avoid a bug in JS.
        return render_template('index.html',
                               reload_status=False,
                               tags=tags)


@ app.route('/start_streaming', methods=["POST"])
def start_streaming():
    if request.method == "POST":
        data = request.json
        listener.set_tags(data)  # Set hashtags given by the user.

        # Start streaming tweets based on the hashtags given.
        stream.start(keyword_list=data,
                     language_list=['en'],
                     follow_list=[],
                     async_status=False)
        return 'OK'


@ app.route('/end_streaming', methods=["POST"])
def end_streaming():
    if request.method == "POST":
        # Stop the streaming
        stream.disconnect()
        return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
