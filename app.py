import twitter_credentials
import tweepy
import itertools
import collections
from flask import Flask, render_template, request
import re

'''
put your twitter api credentials in local file twitter_credentials.py in the format
API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
'''

app = Flask(__name__)


def get_tweets(apitwitter, search_text, num_tweets):

    tweets = tweepy.Cursor(apitwitter.search, q=search_text).items(num_tweets)
    tweets_text = [tweet.text for tweet in tweets]
    return tweets_text


def get_word_counts(tweetstext):
    # Make all tweets one case for easy grouping and split each tweet into seperate words
    tweet_words = [tweet.lower().split() for tweet in tweetstext]

    # List of all words used as strings with duplicates for counting
    words = list(itertools.chain(*tweet_words))

    # Use regex to filter strings containing non-alphabetic
    regex = re.compile(r'^[a-z]*$')
    just_words = list(filter(regex.search, words))

    # Get counts all all tweet words
    word_counts = collections.Counter(just_words)

    # Return top 10 tweet words
    return word_counts.most_common(10)


@app.route('/')
def index():

    # Establish connection to 3rd Party Twitter Api
    auth = tweepy.OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Use 20 for Max Tweets to not exhaust rate limits. Change to 1000 as required in the specs before deployment
    max_tweets = 20

    # Get Search Term From Front End Template
    search_term = request.args.get('q')

    # Check if blank, if so give a default of 'investing'
    if search_term is None:
        search_term = "investing"

    # Ignore Retweets
    search_term += " -filter:retweets"
    filtered_tweets = get_tweets(api, search_term, max_tweets)

    # Get word counts from returned tweets
    word_counts = get_word_counts(filtered_tweets)

    # Pass Tweet Text and Word Counts to Front End Display
    return render_template('home.html', tweets=filtered_tweets, word_counts=word_counts)


if __name__ == '__main__':

    app.run(debug=True)
