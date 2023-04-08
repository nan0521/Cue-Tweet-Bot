import tweepy
import requests
import os
import json
import random

# Twitter API keys and access tokens
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

if(not consumer_key):
    print('consumer_key not found')
if(not consumer_secret):
    print('consumer_key not found')
if(not access_token):
    print('consumer_key not found')
if(not access_token_secret):
    print('consumer_key not found')

