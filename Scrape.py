from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
from FormatCookies import load_and_transform_cookies
from Login import login_to_twitter
from Utilities import NameToID

def get_tweets_by_search(tweets, query, client):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...\n')
        tweets = client.search_tweet(query, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...\n')
        time.sleep(wait_time)
        tweet = tweets.next()

    return tweets

def get_tweets_from_user(tweets, numericalID, client):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...\n')
        tweets = client.get_user_tweets(numericalID, 'Tweets')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...\n')
        time.sleep(wait_time)
        tweets = tweets.next()
    return tweets