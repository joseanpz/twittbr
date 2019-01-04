import tweepy

from db.store_procedures import add_tweet


class StreamListener(tweepy.StreamListener):
    def on_connect(self):
        print('Now we are saving')

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            tweet = status.retweeted_status
        else:
            tweet = status
        try:
            add_tweet(tweet)
        except Exception as exc:
            print(exc)
        # count += 1
        print('Tweet id: {}'.format(tweet.id_str))

    def on_error(self, status_code):
        if status_code == 420:
            return False

