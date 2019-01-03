from pony.orm import db_session
from db.models import Tweet


@db_session
def add_tweet(tweet):
    if not hasattr(tweet, 'text'):
        text = tweet.full_text
    else:
        text = tweet.text
    Tweet(id=tweet.id_str, created_at=tweet.created_at,
          text=text, truncated=tweet.truncated)


