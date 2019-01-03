import tweepy
from datetime import datetime, timedelta

from tweepy_ext.api import BRTweepyAPI
from tweepy_ext.parsers import BRModelParser
from db.store_procedures import add_tweet


consumer_key = 'XRvAAgTcTcPid7HrwAlEyosQV'
consumer_secret = 'YaKSNiuFudkc2Es4WttRF2SYWZtfNjsog11jYct7ZjtJ1vJItU'
access_token = '1075905261410369536-imb7KuNA6G0Q3uNWCml0ulHHsdCvOK'
access_token_secret = 'ji8orRi6tPUjGdGsz8pdWb7liWrHLgsroXQQ3xT0S6PkT'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)
api = BRTweepyAPI(auth)


def tweet_history(tweet):
    in_reply_to_id = tweet.in_reply_to_status_id
    if in_reply_to_id:
        try:
            in_reply_to_status = api.get_status(in_reply_to_id, tweet_mode='extended')
            yield from tweet_history(in_reply_to_status)
        except Exception as e:
            print(e)
    add_tweet(tweet)
    yield tweet


def tweet_histories(tweets_id_list, tweets_root_id_list, min_date, max_id=None):
    try:
        tweets = tweepy.Cursor(api.search, q='banregio', max_id=max_id, tweet_mode='extended').items(20)
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


def tweet_histories_premiere(tweets_id_list, tweets_root_id_list, max_results, from_date, to_date, next=None):
    try:
        if next:
            tweets = api.search_30day(
                post_data={
                    "query": "banregio",
                    'fromDate': from_date,
                    'toDate': to_date,
                    'maxResults': max_results,
                    'next': next
                },
                parser=BRModelParser()
            )
        else:
            tweets = api.search_30day(
                post_data={
                    "query": "banregio",
                    'fromDate': from_date,
                    'toDate': to_date,
                    'maxResults': max_results
                },
                parser=BRModelParser()
            )

        for tweet in tweets:
            if tweet.id in tweets_id_list:
                continue
            new_history = [twt for twt in tweet_history(tweet)]
            tweets_id_list.extend([twt.id for twt in new_history])
            tweets_root_id_list.append({'id': tweet.id, 'created_at': tweet.created_at})
            yield new_history
        if tweets.next:
            yield from tweet_histories_premiere(tweets_id_list, tweets_root_id_list,
                                                max_results, from_date, to_date, tweets.next)
    except Exception as exc:
        print(exc)


tweets_list = []
tweets_id_list = []
tweets_root_id_list = []
histories = []
min_date = datetime.utcnow() - timedelta(days=14)

max_results = 100
from_date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y%m%d%H%M")  # 60 - (60 * 24) * 7
to_date = (datetime.utcnow() - timedelta(minutes=3)).strftime("%Y%m%d%H%M")    # / 60 - (60 * 24) * 3



# {'id': 1077932883959009283, 'created_at': datetime.datetime(2018, 12, 26, 14, 23, 21)}
# {'id': 1076897728339136512, 'created_at': datetime.datetime(2018, 12, 23, 17, 50)}

max_id = None
# max_id = 1076897728339136512 - 1

for history in tweet_histories_premiere(tweets_id_list, tweets_root_id_list, max_results, from_date, to_date):
    print(history)
    histories.append(history)

print('done!')
