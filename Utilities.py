from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

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
def selectChoice() -> str:
    print('...Starting collecting tweets...')
    print('You can either look for specific user\'s tweets or search for a topic')
    choice = input('Type \'user\' to look for a specific user\'s tweets or \'search\' to search for a topic: ')
    return choice

# handle the choice
def handleChoice(choice, client):
    if choice == 'user':
        user_name = input('Enter the user name: ')
        numericalID = NameToID(user_name, client)
        count = input('Enter the number of tweets you want to collect: ')
        return numericalID, count
    elif choice == 'search':
        query = input('Enter the search query: ')
        count = input('Enter the number of tweets you want to collect: ')
        return query, count
    else:
        return None