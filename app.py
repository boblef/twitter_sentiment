from flask import Flask, render_template, request
from lib.TwitterListener import TweetsListener
from lib.Streaming import Streaming
import configparser
import tweepy as tw
import json

app = Flask(__name__)

config_ini = configparser.ConfigParser()
config_ini.read('config/twitter.txt', encoding='utf-8')
API_KEY = config_ini['TWITTER']['API_KEY']
API_SECRET_KEY = config_ini['TWITTER']['API_SECRET_KEY']
ACCESS_TOKEN = config_ini['TWITTER']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config_ini['TWITTER']['ACCESS_TOKEN_SECRET']

auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

listener = TweetsListener()
stream = Streaming(auth, listener)
# stream.start(keyword_list=["USD", "JPY"], language_list=['en'], follow_list=[], async_status=False)


@app.route('/')
def hello():
    name = "Hello"
    return render_template('index.html', name=name)


@app.route('/streaming', methods=["GET", "POST"])
def streaming():
    if request.method == "POST":
        data = request.json
        print(data)
        stream.start(keyword_list=data, language_list=[
                     'en'], follow_list=[], async_status=False)
        return 'OK'


@app.route('/end_streaming', methods=["GET", "POST"])
def end_streaming():
    if request.method == "POST":
        stream.disconnect()
        return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
