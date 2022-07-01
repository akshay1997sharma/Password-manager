#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import true
from password import db, login_manager
from datetime import datetime
from password import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer(), primary_key=True)
    UserName = db.Column(db.String(length=20), nullable=False,
                         unique=True)
    email_id = db.Column(db.String(length=30), nullable=False,
                         unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    mobile_number = db.Column(db.String(length=13), nullable=False,
                              unique=True)
    passwords = db.relationship('Password', backref='owned_user',
                                lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = \
            bcrypt.generate_password_hash(plain_text_password).decode('utf-8'
                )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,
                attempted_password)


class Password(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    WebsiteName = db.Column(db.String(length=20), nullable=False)
    LoginId = db.Column(db.String(length=30), nullable=False,
                        unique=True)
    Password = db.Column(db.String(length=30), nullable=False)
    Last_Updated = db.Column(db.DateTime, default=datetime.now())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
