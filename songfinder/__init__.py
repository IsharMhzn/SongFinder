from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '138cf4922332d7a0e98fc4ac6067238b2273f336'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../songfinder.db'
db = SQLAlchemy(app)

from songfinder import routes