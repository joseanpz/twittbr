from pony.orm import db_session
from db.models import Tweet, User


@db_session
def add_tweet(tweet):
    if user_exists(tweet.user.id_str):
        user = User[tweet.user.id_str]
    else:
        user = User(
            id=tweet.user.id_str,
            created_at=tweet.user.created_at,
            name=tweet.user.name,
            screen_name=tweet.user.screen_name
        )
    entities = tweet.entities
    if hasattr(tweet, 'extended_tweet'):
        text = tweet.extended_tweet['full_text']
        entities = tweet.extended_tweet['entities']
    elif hasattr(tweet, 'full_text'):
        text = tweet.full_text
    else:
        text = tweet.text

    Tweet(
        id=tweet.id_str,
        created_at=tweet.created_at,
        text=text,
        truncated=tweet.truncated,
        in_reply_to_status_id=tweet.in_reply_to_status_id_str,
        in_reply_to_user_id=tweet.in_reply_to_user_id_str,
        in_reply_to_screen_name=tweet.in_reply_to_screen_name,
        entities=entities,
        user=user
    )


@db_session
def user_exists(id):
    return User.exists(id=id)


