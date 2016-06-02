from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask.ext.login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
# from flask.ext.security import SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required

app = Flask(__name__)
# app.config.from_object('config.DevConfig')
app.config.from_object('config.ProdConfig')

babel = Babel(app)
db = SQLAlchemy(app)


