"""Retrieve Tweets, word embeddings, and populate DB"""
import tweepy
import spacy
#import en_core_web_sm
from twitoff.models import DB, Tweet, User
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Grabbing from your own .env file
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# for turning our tweets into an array of numbers
nlp = spacy.load('my_model') # loaded from my_models dir
#nlp = en_core_web_sm.load()
#nlp = spacy.load('en_core_web_sm')
def vectorize_tweet(tweet_text):
  return nlp(tweet_text).vector

def add_or_update_user(username):
  try:
    """Allows us to add/update users to our DB"""
    twitter_user = TWITTER.get_user(username)
    # either updates or adds a user depending upon if they are in the DB
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
    DB.session.add(db_user)

    tweets = twitter_user.timeline(
      count=200, exclude_replies=True,
      include_rts=False, tweet_mode='extended'
    )

    # will update the most recent tweet id to the user
    if tweets:
      db_user.newest_tweet_id = tweets[0].id


    for tweet in tweets:
      #db_tweet = Tweet(id=tweet.id, text=tweet.full_text)
      vectorized_tweet = vectorize_tweet(tweet.full_text)
      db_tweet = Tweet(
        id=tweet.id, text=tweet.full_text,
        vect=vectorized_tweet
      )
      db_user.tweets.append(db_tweet)
      DB.session.add(db_tweet)

  except Exception as e:
    print('Error Processing {}: {}'.format(username, e)) # gives an error
    raise e

  # last thing done is committing changes
  else:
    DB.session.commit()


def insert_example_users():
  # using our functions to add two users
  add_or_update_user('elonmusk')
  add_or_update_user('jackblack')
