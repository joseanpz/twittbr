from twitter_crawler import get_tweets, get_tweets_ht


tweets_gen = get_tweets_ht('banregio', pages=1)

tweets = []

for tweet in tweets_gen:
    tweets.append(tweet)
    for key, value in tweet.items():
        print(key)
        print(value)
        print('----------------------')

print('done!')



#'https://twitter.com/i/search/timeline?vertical=default&q=%23banregio&composed_count=0&' \
#'include_available_features=1&include_entities=1&include_new_items_bar=true&' \
#'interval=30000&lang=es&latent_count=0&min_position='