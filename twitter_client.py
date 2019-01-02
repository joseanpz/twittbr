import tweepy
from tweepy.binder import bind_api
from datetime import datetime, timedelta, timezone


consumer_key = 'XRvAAgTcTcPid7HrwAlEyosQV'
consumer_secret = 'YaKSNiuFudkc2Es4WttRF2SYWZtfNjsog11jYct7ZjtJ1vJItU'
access_token = '1075905261410369536-imb7KuNA6G0Q3uNWCml0ulHHsdCvOK'
access_token_secret = 'ji8orRi6tPUjGdGsz8pdWb7liWrHLgsroXQQ3xT0S6PkT'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class BRTweepyAPI(tweepy.API):

    @property
    def brserach(self):
        """ :reference: https://dev.twitter.com/rest/reference/get/search/tweets
                    :allowed_param:'q', 'lang', 'locale', 'since_id', 'geocode',
                     'max_id', 'since', 'until', 'result_type', 'count',
                      'include_entities', 'from', 'to', 'source'
                """
        return bind_api(
            api=self,
            path='/tweets/search/30day/brsentimentdev.json',
            # path='/tweets/search/fullarchive/brsentimentfulldev.json',
            method='POST',
            payload_type='search_results',
            allowed_param=['q', 'lang', 'locale', 'since_id', 'geocode',
                           'max_id', 'since', 'until', 'result_type',
                           'count', 'include_entities', 'from',
                           'to', 'source', 'fromDate', 'toDate']
        )


# api = tweepy.API(auth)
api = BRTweepyAPI(auth)

# {'id': 1080512600046256128, 'created_at': datetime.datetime(2019, 1, 2, 17, 14, 13)}
# {'id': 1080486739917991936, 'created_at': datetime.datetime(2019, 1, 2, 15, 31, 27)}
# {'id': 1080187753533325312, 'created_at': datetime.datetime(2019, 1, 1, 19, 43, 24)}
# {'id': 1078977017998012416, 'created_at': datetime.datetime(2018, 12, 29, 11, 32, 22)}
# {'id': 1078341452248334337, 'created_at': datetime.datetime(2018, 12, 27, 17, 26, 51)}
# {'id': 1078047915032145921, 'created_at': datetime.datetime(2018, 12, 26, 22, 0, 26)}
# {'id': 1077935054146408449, 'created_at': datetime.datetime(2018, 12, 26, 14, 31, 58)}
# {'id': 1077932883959009283, 'created_at': datetime.datetime(2018, 12, 26, 14, 23, 21)}

# max_id = 1077935054146408449
# try:
#     # tweets = api.home_timeline()
#     tweets = tweepy.Cursor(api.search, q='banregio', max_id=max_id, tweet_mode='extended').items(20)
# except Exception as exc:
#     print(exc)


def tweet_history(tweet):
    in_reply_to_id = tweet.in_reply_to_status_id
    if in_reply_to_id:
        try:
            in_reply_to_status = api.get_status(in_reply_to_id, tweet_mode='extended')
            yield from tweet_history(in_reply_to_status)
        except Exception as e:
            print(e)
    yield tweet


def tweet_histories(tweets_id_list, tweets_root_id_list, min_date, max_id=None):
    try:
        tweets = tweepy.Cursor(api.search, q='banregio', max_id=max_id, tweet_mode='extended').items(20)
        # tweets = api.brserach(post_data={'query': 'banregio'})
        for tweet in tweets:
            if tweet.id in tweets_id_list:
                continue
            new_history = [twt for twt in tweet_history(tweet)]
            tweets_id_list.extend([twt.id for twt in new_history])
            tweets_root_id_list.append({'id': tweet.id, 'created_at': tweet.created_at})
            yield new_history
        if tweets_root_id_list[-1]['created_at'] > min_date:
            max_id = tweets_root_id_list[-1]['id'] - 1
            yield from tweet_histories(tweets_id_list, tweets_root_id_list, min_date, max_id)
    except Exception as exc:
        print(exc)

tweets_list = []
tweets_id_list = []
tweets_root_id_list = []
histories = []
min_date = datetime.utcnow() - timedelta(days=14)

# for tweet in tweets:
#     if tweet.id in tweets_id_list:
#         continue
#     new_history = [twt for twt in tweet_history(tweet)]
#     tweets_id_list.extend([twt.id for twt in new_history])
#     tweets_root_id_list.append({'id': tweet.id, 'created_at': tweet.created_at})
#     tweets_list.append(new_history)
#     print(tweet.full_text)

# {'id': 1077932883959009283, 'created_at': datetime.datetime(2018, 12, 26, 14, 23, 21)}
# {'id': 1076897728339136512, 'created_at': datetime.datetime(2018, 12, 23, 17, 50)}

max_id = None
# max_id = 1076897728339136512 - 1

for history in tweet_histories(tweets_id_list, tweets_root_id_list, min_date, max_id):
    histories.append(history)

print('done!')
