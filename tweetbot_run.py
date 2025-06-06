import tweepy
import requests
import os
import json
import random
import datetime
import pytz
import time
import math


# get Charactor data by json
with open('./CharactorData.json', 'r', encoding='utf-8') as json_file:
    jsondata = json.load(json_file)
    HeroData = jsondata['Charactor']

# find happy birthday
def getBirthdayCharactor(Nowdatetime):
    chardata = list(filter(lambda x: (x['birthMonth'] == Now.month and x['birthDay'] == Now.day and x['id'] < 100), HeroData))

    return chardata

#get Charactor data by datetime
def getCharactor(Nowdatetime):
    #get start DAY
    STARTDAY = datetime.datetime(int(2023),int(6),int(4))
    #cal interval
    interval = Nowdatetime.replace(tzinfo=datetime.timezone.utc) - STARTDAY.replace(tzinfo=datetime.timezone.utc)
    #get charid
    charid = (interval.days % 16) + 1

    # get Charactor data from HeroData
    chardata = list(filter(lambda x: (x['id'] == charid), HeroData))
    costume = (math.floor(interval.days / 16) % chardata[0]['costume']) + 1
    
    return charid, chardata[0]['name'], costume

# connect to X
def connet_twitter(consumer_key, consumer_secret, access_token, access_token_secret, retries = 5):
    if retries <= 0 : return None, None
    try:
        # Authenticate with Twitter API using environment variables
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        # Create a Tweepy API v1.1 object
        api_v1 = tweepy.API(auth = auth)
        # Create a Tweepy API v2 object
        api_v2  = tweepy.Client(access_token = access_token,
                            access_token_secret = access_token_secret,
                            consumer_key = consumer_key,
                            consumer_secret = consumer_secret)
        return api_v1, api_v2
    except Exception as e:
        retries -= 1
        time.sleep(10)
        print(e)
        print('Retrying :', retries)
        return connet_twitter(consumer_key, consumer_secret, access_token, access_token_secret, retries)


def send_tweet(api, tweet, media_ids, counter = 0):
    if counter == 5:
        return
    try:
        api.create_tweet(text = tweet, media_ids=media_ids)
    except Exception as e:
        time.sleep(10)
        print(e)
        print('send tweet retrying :', counter)
        return send_tweet(api, tweet, media_ids, counter = counter+1)

# Twitter API keys and access tokens
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

specialDay = [
    {
        'name' : '謹賀新年',
        'Month' : 1,
        'day' : 1,
        'tag' : 'newYear',
        'file' : 'event_home_007',
    },
    {
        'name' : 'クリスマス',
        'Month' : 12,
        'day' : 24,
        'tag' : 'christmas',
        'file' : 'event_home_001',
    },
    {
        'name' : 'クリスマス②',
        'Month' : 12,
        'day' : 25,
        'tag' : 'christmas',
        'file' : 'event_home_006',
    },
    {
        'name' : 'バレンタイン',
        'Month' : 2,
        'day' : 14,
        'tag' : 'valentine',
        'file' : 'event_home_003',
    },
    {
        'name' : 'ホワイトデー',
        'Month' : 3,
        'day' : 14,
        'tag' : 'whiteday',
        'file' : 'event_home_004',
    },
    {
        'name' : 'ハロウィン',
        'Month' : 10,
        'day' : 31,
        'tag' : 'halloween',
        'file' : 'event_home_005',
    },
]

timeTable = [
    {
        'timeHour': 0,
        'tag' : 'midnight',
        'tweet': 'ホームボイス 深夜',
    },
    {
        'timeHour': 6,
        'tag' : 'morning',
        'tweet': 'ホームボイス 朝',
    },
    {
        'timeHour': 12,
        'tag' : 'noon',
        'tweet': 'ホームボイス 昼',
    },
    {
        'timeHour': 18,
        'tag' : 'night',
        'tweet': 'ホームボイス 夜',
    }
]

if(not consumer_key or not consumer_secret or not access_token or not access_token_secret):
    print('can not find the env')
else :
    api_v1, api_v2 = connet_twitter(consumer_key, consumer_secret, access_token, access_token_secret)

    if api_v1 and api_v2:
        #get datetime
        Now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        #check Special Day
        isSpecialDay = [spday for spday in specialDay if Now.month == spday['Month'] and Now.day == spday['day']]

        media_ids = []

        # 如果是生日
        if(Now.hour == 0):
            hasBirthdayChar = getBirthdayCharactor(Now)
            if len(hasBirthdayChar) > 0:
                hb_tweet = f'本日{Now.month}/{Now.day}は{hasBirthdayChar[0]["name"]}の誕生日！🎂🎉'
                hb_videofile = './happybirthday/hb_%02d.mp4' % (hasBirthdayChar[0]['id'])
                hb_media = api_v1.media_upload(hb_videofile)
                hb_media_ids = []
                hb_media_ids.append(hb_media.media_id)
                api_v2.create_tweet(text = hb_tweet, media_ids=hb_media_ids)

        # 如果是SpecialDay
        # 6 7 8 9  10 11 12 13  14 15 16 17  18 19 20 21
        if len(isSpecialDay) > 0 and Now.hour > 5 and Now.hour < 22:
            SpecialDay = isSpecialDay[0]
            Allchardata = json.load(open('./CharactorData.json', 'r', encoding='utf-8'))
            char = [data for data in Allchardata["Charactor"] if data["id"] == (Now.hour - 5)][0]
            file = './voice/%s/%02d/%s.mp4' % (SpecialDay["tag"], char["id"], SpecialDay["file"]) # 記得改檔案名
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{char["name"]} {SpecialDay["name"]} ホームボイス'
        
        # midnight (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 0:
            charid, charname, costume = getCharactor(Now)
            # file = './voice/midnight/voice_home_midnight_%03d.mp4' % (charid)
            file = './live2d/midnight/%03d/%03d_%02d.mp4' % (charid, charid, costume)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 深夜'

        # morning (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 6:
            charid, charname, costume = getCharactor(Now)
            # file = './voice/morning/voice_home_morning_%03d.mp4' % (charid)
            file = './live2d/morning/%03d/%03d_%02d.mp4' % (charid, charid, costume)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 朝'

        # noon (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 12:
            charid, charname, costume = getCharactor(Now)
            # file = './voice/noon/voice_home_noon_%03d.mp4' % (charid)
            file = './live2d/noon/%03d/%03d_%02d.mp4' % (charid, charid, costume)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 昼'

        # night (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 18:
            charid, charname, costume = getCharactor(Now)
            # file = './voice/night/voice_home_night_%03d.mp4' % (charid)
            file = './live2d/night/%03d/%03d_%02d.mp4' % (charid, charid, costume)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 夜'

        # home voice (不是SpecialDay)
        # elif len(isSpecialDay) == 0 and Now.hour > 8 and Now.hour % 3 == 0:
        #     charid, charname, costume = getCharactor(Now)
        #     vocieid =  ( Now.hour -3 ) /6
        #     vocietext = {1 : '①', 2:'②', 3:'③'}
        #     file = './voice/home/%02d/voice_home_normal_%03d.mp4' % (charid, vocieid)
        #     media = api_v1.media_upload(file)
        #     media_ids.append(media.media_id)
        #     tweet = f'{charname} ホームボイス{vocietext[vocieid]}'

        elif len(isSpecialDay) == 0 and Now.hour % 2 == 0:

            giturl = "https://raw.githubusercontent.com/Cpk0521/CUECardsViewer/master/public/"
            with open('./CardsData.json', 'r', encoding='utf-8') as json_file:
                jsondata = json.load(json_file)
                
                if Now.hour == 8 or Now.hour == 14 or Now.hour == 20:
                    card = random.choice([x for x in jsondata['Cards'] if x['rarity'] == "4" and x['animation'] != ""])
                    file_url = f"{giturl}{card['animation']}"

                    response = requests.get(file_url)
                    filename = 'gacha.mp4'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    media = api_v1.media_upload(filename)
                    media_ids.append(media.media_id)

                    tweet = f"★{card['rarity']}{card['alias']}{card['heroine']} ガチャ動画"
                else :
                    card = random.choice(jsondata['Cards'])
                    #get card image url
                    image_urls = [f"{giturl}{card['image']['Normal']}"]
                    if('Blooming' in card['image']):
                        image_urls.append(f"{giturl}{card['image']['Blooming']}")

                    # media_ids = []
                    for url in image_urls:
                        print(url)
                        response = requests.get(url)
                        filename = 'temp.jpg'
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        media = api_v1.media_upload(filename)
                        media_ids.append(media.media_id)

                    tweet = f"★{card['rarity']}{card['alias']}{card['heroine']}"

        if len(media_ids) > 0 :
            print(tweet)
            res = api_v2.create_tweet(text = tweet, media_ids=media_ids)
            # send_tweet(api_v2, tweet, media_ids)