"""Main app/routig file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User


def create_app():
  """ Creates and Configures a Flask application"""
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://db.sqlite3"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  DB.init_app(app)

  # TODO - make rest of the application
  @app.route('/')
  def root():
    users = User.query.all()
    return render_template("base.html", title="Home", users=User.query.all())

  return app