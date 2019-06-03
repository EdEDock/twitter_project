import config
import tweepy
import itertools
import collections
from flask import Flask, render_template, request
import re
from google.cloud import datastore
from datetime import datetime


'''
put your twitter api credentials in local file config.py in the format
as well as Google Cloud Project name/id
TWITTER_API_KEY = ''
TWITTER_API_SECRET_KEY = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
GOOGLE_PROJECT_ID = ''
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

def log_search(datastore_client, search_term, timestamp, word_counts):

    with datastore_client.transaction():
        incomplete_key = datastore_client.key('Search')

        task = datastore.Entity(key=incomplete_key)

        task.update({'term': search_term, 'timestamp': timestamp, 'wordcounts':word_counts})

        datastore_client.put(task)


@app.route('/')
def index():

    # Establish connection to 3rd Party Twitter Api
    auth = tweepy.OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_SECRET_KEY)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Establish a connection to Google Datastore
    datastore_client = datastore.Client(project=config.GOOGLE_PROJECT_ID)

    # Use 20 for Max Tweets to not exhaust rate limits. Change to 1000 as required in the specs before deployment
    max_tweets = 1000

    # Get Search Term From Front End Template
    search_term = request.args.get('q')

    # Check if blank, if so give a default of 'investing'
    word_counts = ""

    if search_term is None:

        filtered_tweets = []

    elif search_term == "":

        filtered_tweets = ["No Search Term Eneterd"]

    else:

        # Get current timestamp for logging query
        timestamp = datetime.now()

        # Ignore Retweets
        search_filter = search_term + " -filter:retweets"
        filtered_tweets = get_tweets(api, search_filter, max_tweets)

        # Get word counts from returned tweets
        word_counts = get_word_counts(filtered_tweets)

        # Log Search to Google Datastore
        log_search(datastore_client, search_term, timestamp, dict(word_counts))

    # Pass Tweet Text and Word Counts to Front End Display
    return render_template('home.html', tweets=filtered_tweets, word_counts=word_counts)


if __name__ == '__main__':

    app.run(debug=True)
