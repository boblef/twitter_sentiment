[![CircleCI](https://circleci.com/gh/boblef/twitter_sentiment.svg?style=svg)](https://app.circleci.com/pipelines/github/boblef/twitter_sentiment)

## Sentiment Analysis on Tweets

A Flask application where we can enter hashtags and keywords related to tweets we want to stream and in which an NLP model, <strong>FinBERT</strong> which is a pre-trained NLP model to analyze the sentiment of the financial text, does <strong>sentiment analysis</strong> on the tweets in real-time.
We can see the results of the tweets collected containing the hashtags or keywords and their sentiment scores given by FinBERT via Pandas dataFrame.

## How to use

1. Clone this repository to your local.
   ```
   git clone https://github.com/boblef/twitter_sentiment.git
   ```
2. Create a Twitter developer account
   In order to run the Flask application, we need to create a [Twitter developer account](https://developer.twitter.com/en/apply-for-access).
   <br>
3. Set up the cinfig file
   Once you have created a developer account, the next thing you need to do is to set up the config file.
   Copy `twitter.txt` and put it into the `config` folder with the information you need to set up.
   <strong>What you need is as follows:</strong>

   - API KEY
   - SECRET API KEY

   ![APIKEYS](/images/APIKEY_screenshot.JPG)

   - ACCESS TOKEN
   - SECRET ACCESS TOKEN

   ![TOKENS](/images/TOKEN_screenshot.JPG)

    <hr>

   Copy all of them from your Twitter developer dashboard and paste them to `config/twitter.txt`

   ![Twitter_config](/images/twitter_config.png)
   <br>

4. Set up the environment, and run the application
   You can set up the environment in which we run the Flask application either by using Docker or by creating a conda or pip env by yourself.

- Docker
  Build a container
  ```
  docker build -t twitter_sentiment:latest .
  ```
  Run the image
  ```
  docker run -d -p 5000:5000 twitter_sentiment:latest
  ```
  Open up your browser, and copy and paste the link below. The application is supposed to start.
  ```
  http://localhost:5000/
  ```
- Conda
  Create a conda env whose name is going to be `finbert`
  ```
  conda env create -f environment.yml
  ```
  Activate the conda env you just created
  ```
  source activate finbert
  or
  conda activate finbert
  ```
  Run the application
  ```
  python app.py
  ```

## Further Work

- Some of the functionality used in this application can also be used in the Automated Forex Trading Strategy which I have been working on in order to create new features.
- We change the Deep Learning model which gives sentiment scores to tweets to another NLP model which trained on different dataset, if we want to switch the domain we want to use for.

## Reference

- [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/pdf/1908.10063.pdf)
- [Twitter developer site](https://developer.twitter.com/en/apply-for-access)
- [Tweepy](http://docs.tweepy.org/en/latest/)
