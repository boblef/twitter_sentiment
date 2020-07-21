from tweepy import StreamListener
import json
import csv
from os import path


class TweetsListener(StreamListener):

    def __init__(self, export_csv_path, followers_threshold):
        self.export_csv_path = export_csv_path
        self.followers_threshold = followers_threshold
        self.csv_headers = ["created_at", "text",
                            "related_tags", "user_id", "followers_count"]

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
            self.write_csv(processed_data)
        return processed_data

    def process_data(self, raw_data):
        """Pre-Process the data
        tweet object: https://developer.twitter.com/en/docs/\
            tweets/data-dictionary/overview/tweet-object
        """
        followers_count = raw_data["user"]["followers_count"]
        user_verified = raw_data["user"]["verified"]

        # Check we can trust the tweet
        # by checking user verified and followers count
        if user_verified and followers_count > self.followers_threshold:

            text = raw_data["text"]
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
            with open(self.export_csv_path, 'a') as f:
                writer = csv.DictWriter(f, self.csv_headers)
                writer.writerow(data)
        else:  # When a csv hasnt been created yet
            with open(self.export_csv_path, 'w') as f:
                writer = csv.DictWriter(f, self.csv_headers)
                writer.writeheader()
                writer.writerow(data)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        print(status.text)

    def if_error(self, status):
        print(status)
        return True

    def set_tags(self, tags):
        self.tags = tags

    def get_tags(self):
        return self.tags
