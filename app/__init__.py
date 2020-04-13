''' For various imports'''

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from elasticsearch import Elasticsearch
from config import Config
from flask_babel import Babel, lazy_gettext as _l
from celery import Celery
from config import CELERY_CONFIG


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
babel = Babel()

login.login_view = 'web_login'

app = Flask(__name__)
app.config.from_object(Config)


celery = Celery(app.name)
celery.conf.update(CELERY_CONFIG)

db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
babel.init_app(app)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

from app import models, routes

