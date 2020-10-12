"""Main app/routig file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User, insert_example_users


def create_app():
  """ Creates and Configures a Flask application"""

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3" # where DB is stored
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
  DB.init_app(app)

  @app.route('/')
  def root():
    DB.drop_all() # deletes already present databases
    DB.create_all() # creates the database from scratch
    insert_example_users() # calls function within models.py - inserts users
    return render_template("base.html", title="Home", users=User.query.all())

  # when you run the application we havent built any other 
  # functionality other than the users showing up so keep that in mind
  return app