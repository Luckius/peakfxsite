from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from peakfx import db, login_manager, application
from flask_login import UserMixin
import json
from time import time

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate



application = Flask(__name__)
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mpeakfxdb.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
application.config['MAIL_SERVER'] = 'smtp.googlemail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
#application.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#application.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(application)
moment = Moment(application)
migrate = Migrate(application, db, compare_type=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):

    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    joined_day = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    token = db.Column(db.String(60), nullable=False)
    profesional = db.relationship('Profesional', backref='author', lazy=True)







class Messages(db.Model):

    __searchable__ = ['subjects','messages']
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    emails = db.Column(db.Text, nullable=False)
    subjects = db.Column(db.Text)
    messages = db.Column(db.Text, nullable=False)



    def __repr__(self):
        return f"Messages('{self.subjects}', '{self.date_posted}', '{self.messages}')"




class Phonecall(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    emails = db.Column(db.Text, nullable=False)
    phones = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f"Phonecall('{self.names}', '{self.date_posted}', '{self.phones}')"



class Emails(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    emails = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Emails('{self.emails}')"




class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #longitude = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Profesional('{self.content}','{self.date_posted}')"