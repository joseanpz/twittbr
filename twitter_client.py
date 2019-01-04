import tweepy

from tweepy_ext.api import BRTweepyAPI

consumer_key = 'XRvAAgTcTcPid7HrwAlEyosQV'
consumer_secret = 'YaKSNiuFudkc2Es4WttRF2SYWZtfNjsog11jYct7ZjtJ1vJItU'
access_token = '1075905261410369536-imb7KuNA6G0Q3uNWCml0ulHHsdCvOK'
access_token_secret = 'ji8orRi6tPUjGdGsz8pdWb7liWrHLgsroXQQ3xT0S6PkT'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)
api = BRTweepyAPI(auth)



