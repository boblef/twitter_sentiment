from tweepy import StreamListener
import json


class TweetsListener(StreamListener):

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
        self.process_data(data)
        return True

    def process_data(self, raw_data):
        """Pre-Process the data
        tweet object: https://developer.twitter.com/en/docs/\
            tweets/data-dictionary/overview/tweet-object
        """
        # pprint.pprint(raw_data["text"])
        print(raw_data["text"])
        print(raw_data['created_at'])
        # print(raw_data[0]["text"])
        print("#######################")

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        print(status.text)

    def if_error(self, status):
        print(status)
        return True
