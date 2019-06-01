import twitter_credentials
import tweepy

'''
put your twitter api credentials in local file twitter_credentials.py in the format
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
'''

# Establish connection to 3rd Party Twitter Api
auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)