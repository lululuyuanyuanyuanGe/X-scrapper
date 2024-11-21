from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import pandas as pd

# Convert user name to numerical ID
def NameToID(name, client):
    user = client.get_user_by_screen_name(name)
    user_id = user.id
    return user_id

# Set up csv files
def setUpCSV():
    with open('tweet.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_Count', 'User_Name', 'Tweet_Text', 'Created_At', 'Retweet_Count', 'Favorite_Count'])

# Let's user select a choice
def selectChoice(client) -> str:
    while True:
        choice = input('Type \'user\' to look for a specific user\'s tweets or \'search\' to search for a topic: ')
        choice = choice.lower()
        if choice == 'q':
            exit()
        result = handleChoice(choice, client)
        if result != None:
            search, tweet_max = result
            return search, tweet_max, choice

# handle the choice
def handleChoice(choice, client):
    if choice == 'user':
        user_name = input('Enter the user name: ')
        if user_name == 'q':
            exit()
        numericalID = NameToID(user_name, client)
        count = input('Enter the number of tweets you want to collect: ')
        if count == 'q':
            exit()
        return numericalID, count
    elif choice == 'search':
        query = input('Enter the search query: ')
        if query == 'q':
            exit()
        count = input('Enter the number of tweets you want to collect: ')
        if count == 'q':
            exit()
        return query, count
    else:
        print('Invalid choice. Please try again.')
        return None
    
# Get content from tweet_csv
def get_content_from_tweet_csv(file_name):
    df = pd.read_csv(file_name)
    df['Tweet_Text'] = df['Tweet_Text'].str.replace(r'\s+', ' ', regex=True).str.strip()    
    tweet_cotent = ''
    for i, content in enumerate(df['Tweet_Text'], start=1):
        tweet_cotent += f"{i}: {content}\n"
    return tweet_cotent

# Read the content from tweet.csv
def print_csv_content(file_name):

    df = pd.read_csv(file_name)
        
    df['Tweet_Text'] = df['Tweet_Text'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    for i, content in enumerate(df['Tweet_Text'], start=1):
        print(f"{i}: {content}")

    