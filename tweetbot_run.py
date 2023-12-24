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
    except:
        retries -= 1
        print('Retrying.', retries)
        time.sleep(5)
        return connet_twitter(consumer_key, consumer_secret, access_token, access_token_secret, retries)


# def send_tweet(tweet, media_ids, counter = 0):
#     if counter == 5:
#         return
#     res = api_v2.create_tweet(text = tweet, media_ids=media_ids)
#     if not res.status_code == 200:
#         time.sleep(5)
#         return send_tweet(tweet, media_ids, counter = counter+1)

# Twitter API keys and access tokens
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

specialDay = [
    {
        'name' : 'New Year',
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
    # {
    #     'name' : 'Valentine',
    #     'Month' : 2,
    #     'day' : 14,
    #     'tag' : 'valentine'
    # },
    # {
    #     'name' : 'White Day',
    #     'Month' : 3,
    #     'day' : 14,
    #     'tag' : 'whiteday'
    # },
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
        
        # 如果是SpecialDay
        if len(isSpecialDay) > 0 and Now.hour > 7:
            SpecialDay = isSpecialDay[0]
            Allchardata = json.load(open('./CharactorData.json', 'r', encoding='utf-8'))
            char = [data for data in Allchardata["Charactor"] if data["id"] == (Now.hour - 7)][0]
            file = './voice/%s/%02d/%s.mp4' % (SpecialDay["tag"], char["id"], SpecialDay["file"]) # 記得改檔案名
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{char["name"]} {SpecialDay["name"]} ホームボイス'
            res = api_v2.create_tweet(text = tweet, media_ids=media_ids)
        
        # midnight (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 0:
            charid, charname = getCharactor(Now)
            file = './voice/midnight/voice_home_midnight_%03d.mp4' % (charid)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 深夜'

        # morning (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 6:
            charid, charname = getCharactor(Now)
            file = './voice/morning/voice_home_morning_%03d.mp4' % (charid)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 朝'

        # noon (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 12:
            charid, charname = getCharactor(Now)
            file = './voice/noon/voice_home_noon_%03d.mp4' % (charid)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 昼'

        # night (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour == 18:
            charid, charname = getCharactor(Now)
            file = './voice/night/voice_home_night_%03d.mp4' % (charid)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス 夜'

        # home voice (不是SpecialDay)
        elif len(isSpecialDay) == 0 and Now.hour > 8 and Now.hour % 3 == 0:
            charid, charname = getCharactor(Now)
            vocieid =  ( Now.hour -3 ) /6
            vocietext = {1 : '①', 2:'②', 3:'③'}
            file = './voice/home/%02d/voice_home_normal_%03d.mp4' % (charid, vocieid)
            media = api_v1.media_upload(file)
            media_ids.append(media.media_id)
            tweet = f'{charname} ホームボイス{vocietext[vocieid]}'

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
                    print(url)
                    response = requests.get(url)
                    filename = 'temp.jpg'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    media = api_v1.media_upload(filename)
                    media_ids.append(media.media_id)

                tweet = f"★{card['rarity']}{card['alias']}{card['heroine']}"

        res = api_v2.create_tweet(text = tweet, media_ids=media_ids)