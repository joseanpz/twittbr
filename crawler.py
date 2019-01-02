from twitter_crawler import get_tweets, get_tweets_ht
import pandas as pd

tweets_gen = get_tweets_ht('banregio', pages=3)

tweets = []

for tweet in tweets_gen:
    tweet['text'] = tweet['text'].replace("\n", " ")
    tweets.append(tweet)
    for key, value in tweet.items():
        print(key)
        print(value)
        print('----------------------')
tweets_df = pd.DataFrame(tweets)
print('done!')
tweets_df_wo_duplicates = tweets_df.drop_duplicates('time')
tweets_df_wo_duplicates.sort_values(by='time', ascending=False).to_csv('test.csv')

GCP_TWETBR_API_KEY = "AIzaSyA_Bo83CczOiy_jFiknCF99_t3EOcUre7Y"



#'https://twitter.com/i/search/timeline?vertical=default&q=%23banregio&composed_count=0&' \
#'include_available_features=1&include_entities=1&include_new_items_bar=true&' \
#'interval=30000&lang=es&latent_count=0&min_position='