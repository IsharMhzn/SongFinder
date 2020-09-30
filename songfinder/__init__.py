from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
import redis, rq

from songfinder.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
socketapp = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

rds = redis.Redis()
task_q = rq.Queue(connection=rds)

from songfinder import routes, models