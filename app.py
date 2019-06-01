import twitter_credentials
import tweepy

'''
put your twitter api credentials in local file twitter_credentials.py in the format
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
'''


def get_tweets(apitwitter, search_text, num_tweets):

    tweets = tweepy.Cursor(apitwitter.search, q=search_text).items(num_tweets)
    tweets_text = [tweet.text for tweet in tweets]
    return tweets_text


if __name__ == '__main__':

    # Establish connection to 3rd Party Twitter Api
    auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    search_term = "investing"
    # Use 20 for Max Tweets to not exhaust rate limits. Change to 1000 as required in the specs before deployment
    max_tweets = 20

    filtered_tweets = get_tweets(api, search_term, max_tweets)

    # Print Returned Tweets
    for index, tweet in enumerate(filtered_tweets):
        print("Tweet Number: {} Tweet Text:{} ".format(index+1, tweet))