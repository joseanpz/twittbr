import tweepy

from twitter_client import api
from stream import StreamListener


stream = tweepy.Stream(auth=api.auth, listener=StreamListener())

# while True:
#     try:
stream.filter(track=['banregio'])
#     except Exception as e:
#         print(e)
#        continue
