import csv
from random import randint
import pandas as pd
import sys

# Convert user name to numerical ID
def NameToID(name, client):
    user = client.get_user_by_screen_name(name.lower())
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
        print('Type \'user\' to look for a specific user\'s tweets or \'search\' to search for a topic: ')
        choice = sys.stdin.readline().strip()
        if choice.lower() == 'q':
            exit()
        result = handleChoice(choice, client)
        if result != None:
            search, tweet_max = result
            return search, tweet_max, choice

# handle the choice
def handleChoice(choice, client):
    if choice == 'user':
        print('Enter the user name: ')
        user_name = sys.stdin.readline().strip()
        if user_name.lower() == 'q':
            exit()
        numericalID = NameToID(user_name, client)
        print('Enter the number of tweets you want to collect: ')
        count = sys.stdin.readline().strip()
        if count.lower() == 'q':
            exit()
        return numericalID, count
    elif choice == 'search':
        print('Enter the search query: ')
        query = sys.stdin.readline().strip()
        if query.lower() == 'q':
            exit()
        print('Enter the number of tweets you want to collect: ')
        count = sys.stdin.readline().strip()
        if count.lower() == 'q':
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

    