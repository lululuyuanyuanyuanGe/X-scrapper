from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
from FormatCookies import load_and_transform_cookies


MINIMUM_TWEETS = 100
QUERY = '(from:lidangzzz)'

def get_tweets(tweets):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...\n')
        tweets = client.search_tweet(QUERY, product='TOP')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...\n')
        time.sleep(wait_time)
        tweet = tweets.next()


    return tweets

# Initialize Client
client = Client(language='en-US')

# Load and set cookies
cookies_dict = load_and_transform_cookies('cookies.json')
client.set_cookies(cookies_dict)

#* Create a csv file to store the tweets
with open('tweet.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_Count', 'User_Name', 'Tweet_Text', 'Created_At', 'Retweet_Count', 'Favorite_Count'])

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset} ...\n')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print(f'{datetime.now()} - No more tweets found\n')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

        with open('tweet.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)

    print(f'{datetime.now()} - Got {tweet_count} tweets\n')

