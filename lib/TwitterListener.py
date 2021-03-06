from tweepy import StreamListener
from lib.finbert import predict
import json
import csv
from os import path


class TweetsListener(StreamListener):

    def __init__(self, export_csv_path, followers_threshold, model):
        self.export_csv_path = export_csv_path
        self.followers_threshold = followers_threshold
        self.csv_headers = ["created_at", "text", "related_tags", "logit",
                            "prediction", "sentiment_score", "followers_count",
                            "user_id"]
        self.model = model
        self.fc_threshold = 1000
        self.verification = True
        self.tags = None

    def on_connect(self):
        """Called once connected to streaming server.
        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        pass

    # we override the on_data() function in StreamListener
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        processed_data = self.process_data(data)

        if processed_data is not None:  # When the data is trustable
            print(processed_data)
            prediction_result = self.get_prediction(processed_data["text"])
            processed_data.update(prediction_result)
            self.write_csv(processed_data)
        return processed_data

    def process_data(self, raw_data):
        """Pre-Process the data
        tweet object: https://developer.twitter.com/en/docs/\
            tweets/data-dictionary/overview/tweet-object
        """
        followers_count = raw_data["user"]["followers_count"]
        user_verified = raw_data["user"]["verified"]

        if not self.verification:  # When user accept tweets of all users
            user_verified = True

            # Check we can trust the tweet
            # by checking user verified and followers count
        if user_verified and followers_count >= self.fc_threshold:
            # Try to get full text if there are more than 140 chars.
            try:
                text = raw_data.extended_tweet["full_text"]
                print("Full Text: ", text)
            except AttributeError:
                text = raw_data["text"]
                print("Not Full Text: ", text)

            created_at = raw_data["created_at"]
            user_id = raw_data["user"]["id"]
            related_tags = [tag for tag in self.tags if tag in text]

            return {"created_at": created_at,
                    "text": text,
                    "related_tags": related_tags,
                    "user_id": user_id,
                    "followers_count": followers_count}
        else:
            return None

    def write_csv(self, data):
        """Add a row to a csv"""
        if path.exists(self.export_csv_path):  # there is already a csv file
            with open(self.export_csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, self.csv_headers)
                writer.writerow(data)
        else:  # When a csv hasnt been created yet
            with open(self.export_csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, self.csv_headers)
                writer.writeheader()
                writer.writerow(data)

    def get_prediction(self, text):
        """
        Return
        batch_result = {'logit': list(logits),
                        'prediction': predictions,
                        'sentiment_score': sentiment_score}
        """
        return predict(text, self.model)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        pass

    def if_error(self, status):
        print(status)
        return True

    def set_tags(self, tags):
        self.tags = self.add_tags(tags)

    def set_threshold(self, threshold):
        self.fc_threshold = threshold

    def set_verification(self, verification):
        self.verification = verification

    def add_tags(self, tags):
        """
        Add more tags related to the given tags such as small letters of them
        """
        lower_tags = [tag.lower() for tag in tags
                      if tag.lower() not in tags]
        tags += lower_tags
        return tags

    def get_tags(self):
        return self.tags
