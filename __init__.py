#!/usr/bin/python
# -*- coding: utf-8 -*-
import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password.db'
app.config['SECRET_KEY'] = 'df17313966c5f968fb9c9255'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from password import routes
