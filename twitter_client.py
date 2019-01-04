import tweepy
from datetime import datetime, timedelta

from tweepy_ext.api import BRTweepyAPI
from tweepy_ext.parsers import BRModelParser
from db.store_procedures import add_tweet
from db.models import Tweet, orm


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
    try:
        add_tweet(tweet)
    except Exception as e:
        print(e)
        raise StopIteration
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


def tweet_histories_premiere(query, from_date, to_date, max_results=100,
                             max_num_req=10, next=False,):
    with orm.db_session:
        tweets_id_list = list(orm.select(int(tweet.id) for tweet in Tweet)[:])
    try:
        post_data = {
            'query': query,
            'fromDate': from_date,
            'toDate': to_date,
            'maxResults': max_results
        }
        if next:
            post_data['next'] = next
        # tweets = api.search_30day(post_data=post_data, parser=BRModelParser())
        tweets = api.search_fullarchive(post_data=post_data, parser=BRModelParser())

        max_num_req -= 1
        for tweet in tweets:
            if hasattr(tweet, 'retweeted_status'):
                tweet = tweet.retweeted_status
            if tweet.id in tweets_id_list:
                continue
            new_history = [twt for twt in tweet_history(tweet)]
            tweets_id_list.extend([twt.id for twt in new_history])
            yield new_history
        if tweets and tweets.next and max_num_req > 0:
            yield from tweet_histories_premiere(query, from_date, to_date, max_results,
                                                max_num_req, tweets.next)
    except Exception as exc:
        print(exc)


tweets_list = []
tweets_root_id_list = []
histories = []
min_date = datetime.utcnow() - timedelta(days=14)


# max_results = 100

query = "banregio OR #banregio"

# 30day endpoint
# from_date = (datetime.utcnow() - timedelta(days=31)).strftime("%Y%m%d%H%M")
# to_date = (datetime.utcnow() - timedelta(minutes=3)).strftime("%Y%m%d%H%M")

# fullarchive endpont
orm.set_sql_debug(True)
with orm.db_session:
    # query examples
    # sel = orm.select(twt for twt in Tweet if twt.id not in
    #                  orm.select(t.in_reply_to_status_id for t in Tweet))
    #
    # sel2 = orm.select(twt for twt in Tweet if twt.in_reply_to_status_id == '978778172492828672')[:]
    to_date_raw = orm.select(twt.created_at for twt in Tweet)[:][-1]

to_date = to_date_raw.strftime("%Y%m%d%H%M")
from_date = (to_date_raw - timedelta(days=31)).strftime("%Y%m%d%H%M")


for history in tweet_histories_premiere(query, from_date, to_date):
    print(history)
    histories.append(history)

print('done!')
