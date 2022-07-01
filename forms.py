#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, \
    ValidationError
import password
from password.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = \
            User.query.filter_by(UserName=username_to_check.data).first()
        if user:

            raise ValidationError('User name already exists try with new user name'
                                  )

    def validate_email(self, email_to_check):
        emailid = \
            User.query.filter_by(email_id=email_to_check.data).first()
        if emailid:
            raise ValidationError('email id already exists try with new email id'
                                  )

    username = StringField(label='username', validators=[Length(min=2,
                           max=20), DataRequired()])
    email = StringField(label='email', validators=[Email(),
                        DataRequired()])
    password1 = PasswordField(label='Password 1',
                              validators=[Length(min=2),
                              DataRequired()])
    password2 = PasswordField(label='Confirm Password',
                              validators=[EqualTo('password1'),
                              DataRequired()])

    mobile_number = StringField(label='mobile number',
                                validators=[Length(min=13, max=13),
                                DataRequired()])

    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):

    username = StringField(label='username',
                           validators=[DataRequired()])
    password = PasswordField(label='username',
                             validators=[DataRequired()])
    submit = SubmitField(label='Login in')


class UpdatePasswordForm(FlaskForm):

    submit = SubmitField(label='New Password')


class DeletePasswordForm(FlaskForm):

    submit = SubmitField(label='Delete Password')


class AddPasswordForm(FlaskForm):

    WebsiteName = StringField(label='WebsiteName',
                              validators=[Length(min=2, max=20),
                              DataRequired()])
    LoginId = StringField(label='LoginId', validators=[Email(),
                          DataRequired()])
    Password = PasswordField(label='Password',
                             validators=[Length(min=2)])
    submit = SubmitField(label='Add New Password details')


class VerifyotpForm(FlaskForm):

    otp = StringField(label='Enter Otp',
                              validators=[Length(min=6, max=6),
                              DataRequired()])
    
    submit = SubmitField(label='Submit')

