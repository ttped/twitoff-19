# twitoff-19
Flask web application that compares users.

## Setup pipenv

```sh
py -m pipenv install flask jinja2 flask_sqlalchemy flask_migrate python-dotenv spacy psycopg2-binary gunicorn
```

## Database Setup
Setup the database:
```sh
FLASK_APP=web_app flask db init
#> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate
#> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade
 #> creates the specified tables
```

## Running the app
Run commandline in parent folder
twitoff represents the folder twitoff
```sh
FLASK_APP=twitoff py -m flask run
```

py -m spacy download en_core_web_sm

# Creating spacy NLP model
in twitoff-19 directory run
```sh
py -i
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp
nlp.to_disk('my_model/')
nlp = spacy.load('my_model')
word2vect = nlp('this is some example text of a tweet').vector
word2vect
```


# Other stuff?

```sh
touch Procfile #Run in same place as git, pipfile, .env, etc...
```