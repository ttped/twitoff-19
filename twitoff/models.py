"""SQLAlchemy models and utility fucntions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB = SQLAlchemy()

migrate = Migrate()

# User table with columns id and name
class User(DB.Model):
  """Twitter Users corresponding to Tweets"""
  id = DB.Column(DB.BigInteger, primary_key=True)
  name = DB.Column(DB.String, nullable=False)
  newest_tweet_id = DB.Column(DB.BigInteger)

  def __repr__(self):
    return "<User: {}>".format(self.name)


# Tweet table with columns id, text, and user_id
class Tweet(DB.Model):
  """Tweet related to a user"""
  id = DB.Column(DB.BigInteger, primary_key=True)
  text = DB.Column(DB.Unicode(300))
  vect = DB.Column(DB.PickleType, nullable=False)
  user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
  user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

  def __repr__(self):
    return "<Tweet: {}>".format(self.text)


# example users but remember they dont have tweets
def insert_example_users():
  """ Example users """
  bill = User(id=1, name="BillGates")
  elon = User(id=2, name="ElonMusk")
  DB.session.add(bill)
  DB.session.add(elon)
  DB.session.commit()
