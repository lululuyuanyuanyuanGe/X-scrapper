from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
from FormatCookies import load_and_transform_cookies
from Login import login_to_twitter
from Utilities import setUpCSV, selectChoice, handleChoice, print_csv_content
from Scrape import get_tweets_by_search, get_tweets_from_user
from chatGPT import summarize_tweet

def main():
    global Login
    # Initialize Client
    client = Client(language='en-US')

    # Login to Twitter
    if not Login:
        Login = True
        login_to_twitter()
        # Load and set cookies
        cookies_dict = load_and_transform_cookies('cookies.json')
        client.set_cookies(cookies_dict)

        # Set up csv files
        setUpCSV()

    print('...Starting collecting tweets...')
    print('You can either look for specific user\'s tweets or search for a topic')

    # Let user select a choice to search for tweets
    search, tweet_max, choice = selectChoice(client)
    tweet_max = int(tweet_max)

    tweet_count = 0
    tweets = None

    while tweet_count < tweet_max:
        try:
            if choice == 'search':
                tweets = get_tweets_by_search(tweets, search, client)
            elif choice == 'user':
                tweets = get_tweets_from_user(tweets, search, client)
    
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
            if tweet_count >= tweet_max:
                break
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.full_text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

            with open('tweet.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)
        if tweet_count >= tweet_max:
            break
        print(f'{datetime.now()} - Got {tweet_count} tweets\n')

    print_csv_content("tweet.csv")
    reply = summarize_tweet("tweet.csv")
    print(reply)

if __name__ == '__main__':
    Login = False
    while True:
        main()