from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from celery import Celery
import os

import redis
from rq import Queue

# redis config
r = redis.Redis()
q = Queue('default', connection=r)

# flask initailization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# DB settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

app.config["ALLOWED_EXTENSIONS"] = {"MP4", "MOV"}
app.config["MAX_VIDEO_FILESIZE"] = 1024 * 1024 * 1024

def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

# Login settings

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

# Blueprints registering 

from myproject.core.views import core
from myproject.users.views import users
from myproject.error_pages.handers import error_pages
from myproject.project.name_upload import name_upload
from myproject.project.training import training

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(name_upload)
app.register_blueprint(training)