#!/usr/bin/python
# -*- coding: utf-8 -*-

from crypt import methods
from http import server
from xmlrpc import client
from password import app
from flask import render_template, redirect, url_for, flash
import password
from password.forms import RegisterForm, LoginForm, UpdatePasswordForm, \
    DeletePasswordForm, AddPasswordForm,VerifyotpForm
from password.models import User, Password
from password import db
import pyotp
from twilio.rest import Client
import random
from flask_login import login_user, logout_user, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/password_page', methods=['POST', 'GET'])
def password_page():
    update_form = UpdatePasswordForm()
    delete_form = DeletePasswordForm()
    passwords = Password.query.filter_by(owner=current_user.id)
    return render_template('password.html', passwords=passwords,
                           update_form=update_form)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(UserName=form.username.data,
                              email_id=form.email.data,
                              password=form.password1.data,
                              mobile_number=form.mobile_number.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Succesfully created and logged  in as {user_to_create.UserName} '
              , category='success')

        return redirect(url_for('password_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash('{err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = \
            User.query.filter_by(UserName=form.username.data).first()
        if attempted_user \
            and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Succesfully logged in as {attempted_user.UserName}',
                  category='success')
            return redirect(url_for('getotp_page'))
        else:
            flash('Username ans password dont match', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out', category='info')
    return redirect(url_for('home_page'))


@app.route('/addpassword', methods=['POST', 'GET'])
def add_password_page():
    form = AddPasswordForm()
    if form.validate_on_submit():
        password_to_create = \
            Password(WebsiteName=form.WebsiteName.data,
                     LoginId=form.LoginId.data,
                     Password=form.Password.data, owner=current_user.id)
        db.session.add(password_to_create)
        db.session.commit()

        flash('Succesfully added new passwords details} ',
              category='success')

        return redirect(url_for('password_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash('{err_msg}', category='danger')
    return render_template('addpassword.html', form=form)


@app.route('/getotp', methods=['POST', 'GET'])
def getotp_page():

    generated_number = random.randrange(100000,999999)
    
    account_sid='AC99e11b548e8d0b362bf4baabf6f42569'
    auth_token= '55f7452a3d642b8ad135481d9b819143'
    client=Client(account_sid,auth_token)
    # client.message.create(
    #                     to = current_user.mobile_number
    #                     from = "+131255555"
    #                     body = generated_number)

    form = VerifyotpForm()
    print("this got generated"+str(generated_number))
    if form.validate_on_submit():
        enterted_otp = form.otp.data
        
        print("this got entered"+str(enterted_otp))
        if(generated_number==enterted_otp):
            flash('Succesfully added new passwords details} ',
              category='success')

            return redirect(url_for('password_page'))
        else:
            flash('Wrong Otp',
              category='danger')
            return redirect(url_for('logout_page'))

    return render_template('verifyotp.html', form=form)