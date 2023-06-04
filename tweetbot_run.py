import tweepy
import requests
import os
import json
import random
import datetime
import pytz

#get Charactor data by datetime
def getCharactor(Nowdatetime):
    #get start DAY
    STARTDAY = datetime.datetime(int(2023),int(6),4)
    #cal interval
    interval = Nowdatetime.replace(tzinfo=datetime.timezone.utc) - STARTDAY.replace(tzinfo=datetime.timezone.utc)
    #get charid
    charid = (interval.days % 16) + 1

    with open('./CharactorData.json', 'r', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        HeroData = jsondata['Charactor']
        charname = list(filter(lambda x: (x['id'] == charid), HeroData))
    
    return charid, charname[0]['name']


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
    # Create a Tweepy API v1.1 object
    api_v1 = tweepy.API(auth = auth)
    # Create a Tweepy API v2 object
    api_v2  = tweepy.Client(access_token = access_token,
                        access_token_secret = access_token_secret,
                        consumer_key = consumer_key,
                        consumer_secret = consumer_secret)

    #get datetime
    Now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    media_ids = []

    if Now.hour == 0:
        # midnight
        charid, charname = getCharactor(Now)
        file = './voice/midnight/voice_home_midnight_%03d.mp4' % (charid)
        media = api_v1.media_upload(file)
        media_ids.append(media.media_id)
        tweet = f'{charname} ホームボイス 深夜'
    elif Now.hour == 6:
        # morning
        charid, charname = getCharactor(Now)
        file = './voice/morning/voice_home_morning_%03d.mp4' % (charid)
        media = api_v1.media_upload(file)
        media_ids.append(media.media_id)
        tweet = f'{charname} ホームボイス 朝'
    elif Now.hour == 12:
        # noon
        charid, charname = getCharactor(Now)
        file = './voice/noon/voice_home_noon_%03d.mp4' % (charid)
        media = api_v1.media_upload(file)
        media_ids.append(media.media_id)
        tweet = f'{charname} ホームボイス 昼'
    elif Now.hour == 18:
        # night
        charid, charname = getCharactor(Now)
        file = './voice/night/voice_home_night_%03d.mp4' % (charid)
        media = api_v1.media_upload(file)
        media_ids.append(media.media_id)
        tweet = f'{charname} ホームボイス 夜'
    else:
        with open('./CardsData.json', 'r', encoding='utf-8') as json_file:
            jsondata = json.load(json_file)
            card = random.choice(jsondata['Cards'])

            #get card image url
            giturl = "https://raw.githubusercontent.com/Cpk0521/CUECardsViewer/master/public/"
            image_urls = [f"{giturl}{card['image']['Normal']}"]
            if('Blooming' in card['image']):
                image_urls.append(f"{giturl}{card['image']['Blooming']}")

            # media_ids = []
            for url in image_urls:
                response = requests.get(url)
                filename = 'temp.jpg'
                with open(filename, 'wb') as f:
                    f.write(response.content)
                media = api_v1.media_upload(filename)
                media_ids.append(media.media_id)

            tweet = f"★{card['rarity']}{card['alias']}{card['heroine']}"

    res = api_v2.create_tweet(text = tweet, media_ids=media_ids)

