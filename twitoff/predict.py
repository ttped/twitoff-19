"""Prediction of Users based on tweet embeddings"""

import numpy
import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.models import User
from twitoff.twitter import vectorize_tweet

def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and return which user is more liekly to say a given hypo_tweet_text

    Example run: predict_user('jackblack', 'hillaryclinton', 'I like politics')
    Return 0 (user0_name) or 1 (user1_name)
    """

    user1 = User.query.filter(User.name==user1_name).one()
    user0 = User.query.filter(User.name==user0_name).one()
    user0_vect = np.array([tweet.vect for tweet in user0.tweets])
    user1_vect = np.array([tweet.vect for tweet in user1.tweets])

    vect = np.vstack([user0_vect, user1_vect])
    labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    log_reg = LogisticRegression().fit(vect, labels)
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(np.array(hypo_tweet_vect).reshape(1, -1))
