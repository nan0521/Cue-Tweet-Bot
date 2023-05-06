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


if(not consumer_key or not consumer_secret or not access_token or not access_token_secret):
    print('can not find the env')
else :
    # Authenticate with Twitter API using environment variables
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)

    # Create a Tweepy API object
    api = tweepy.API(auth)

    with open('./CardsData.json', 'r', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        num = random.randint(0, len(jsondata['Cards']))
        card = jsondata['Cards'][num]

    giturl = "https://raw.githubusercontent.com/Cpk0521/CUECardsViewer/master/public/"

    image_urls = [f"{giturl}{card['image']['Normal']}"]

    if(card['image']['Blooming']):
        image_urls.append(f"{giturl}{card['image']['Blooming']}")
    
    media_ids = []
    for url in image_urls:
        response = requests.get(url)
        filename = 'temp.jpg'
        with open(filename, 'wb') as f:
            f.write(response.content)
        media = api.media_upload(filename)
        media_ids.append(media.media_id)


    # Create a Tweet
    tweet = f"★{card['rarity']}{card['alias']}{card['heroine']}"
    api.update_status(status=tweet, media_ids=media_ids)

