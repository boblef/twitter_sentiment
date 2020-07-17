import tweepy as tw


class Streaming():
    def __init__(self, auth, listener):
        self.stream = tw.Stream(auth=auth, listener=listener)

    def start(self, keyword_list, language_list,
              follow_list, async_status=False):
        print("Start Streaming....")
        self.stream.filter(track=keyword_list, languages=language_list,
                           follow=follow_list, is_async=async_status)

    def userstream(self, user_list):
        self.stream.userstream(track=user_list)

    def disconnect(self):
        self.stream.disconnect()
        print("Stopped streaming.")
