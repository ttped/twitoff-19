"""Main app/routig file for Twitoff"""

from flask import Flask, render_template, request
from twitoff.models import DB, User, migrate
from twitoff.twitter import insert_example_users
from os import getenv
from twitoff.predict import predict_user

def create_app():
    """ Creates and Configures a Flask application"""

    app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    migrate.init_app(app, DB)


    @app.route('/')
    def root():
        #new_user = User(id=1, name="nick", newest_tweet_id=1)
        #DB.session.add(new_user)
        #DB.session.commit()
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user1'],
        request.values['user2']])
        message = ""
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0, user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=""):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/update')
    def update():
        # adds our users
        insert_example_users()
        return render_template('base.html', title="Home", users=User.query.all())


    @app.route('/reset')
    def reset():
        # resets database
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')


    return app
