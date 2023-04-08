# Cue-Tweet-Bot
This is a simple Twitter bot that can post the tweet about game CUE! Card. 
It was developed using the **Python** and utilizes the **tweepy** module to interact with the Twitter API. 
The bot can be set to run on a schedule using **GitHub Action**.

# How to Setup / Use
This requires the use of both GitHub Action and the Twitter API to function properly.

## Twitter Api setup
You need a Twitter Developer account to get the api key.

If you haven't already, you can go to [https://developer.twitter.com/en/apps](https://developer.twitter.com/en/apps)  and click on **Apply for a  Developer Account**. Follow the prompts to create your account.

Then, you will need to create a Twitter App. This app will serve as your bot. Click on **Create an App** and follow the prompts to create your app.

After that, you can go to your Twitter App dashboard to generate your API keys and access tokens. 
1. Go to Twitter App **Setting** page to find out the  **User authentication settings** option to edit **App permissions**, **Type of App** and  **App info**. **App permissions** must to change to **Read and write** option. and Save it.
2. Go to Twitter App **Keys and tokens** page to generate the **Consumer Keys** and  **Authentication Tokens**, and save it.

## Github Action environments setup

you need to go to your repository **Setting** page to find **Secrets and variables** option and select the **Action** to create the environments.

then, click the **New repository secret** to append the following four variables
1. TWITTER_CONSUMER_KEY 
2. TWITTER_CONSUMER_SECRET 
3. TWITTER_ACCESS_TOKEN 
4. TWITTER_ACCESS_TOKEN_SECRET 

## Edit YML file 
You can set the schedule in yml to execute the python file

If you want to change the schedule, you need to modify the following part
```yml
on:
#   schedule:
#     - cron: '0 * * * *'
	workflow_dispatch :
```
If you don't know how to set, you can use  [ schedule expression editor](https://crontab.guru/) to set it

#
