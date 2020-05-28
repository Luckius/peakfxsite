from datetime import datetime
import os
from flask import Flask,render_template, url_for, flash, redirect, request, abort,g
from flask_login import login_user, current_user, logout_user, login_required,login_manager
#from peakfx import application, db, bcrypt, mail
from forms import RegistrationForm, LoginForm
from models import User, Messages, Phonecall, Emails,Profesional
import secrets
import smtplib
import imghdr
from email.message import EmailMessage
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
#from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate




"""application = Flask(__name__)
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
application.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
application.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(application)
moment = Moment(application)
migrate = Migrate(application, db, compare_type=True)"""


#import models 
from models import *


@application.route("/")
def index():
    return render_template('index.html')


@application.route("/news")
def news():
   
    posts = Profesional.query.all() 
    return render_template('news.html',posts=posts)



@application.route("/elements")
def elements():
    return render_template('elements.html')



@application.route("/contact")
def contact():
    return render_template('contact.html')



@application.route("/about")
def about():
    return render_template('about.html')



@application.route("/services")
def services():
    return render_template('services.html')



@application.route("/investment")
def investment():
    return render_template('investment.html')


@application.route("/financial")
def financial():
    return render_template('financial.html')

@application.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')




def send_email_to_admin(userToken,userName,userEmail):    
    
    EMAIL_ADDRESS = "peakfxceo@gmail.com"
    EMAIL_PASSWORD = "tanzanianigeria"

    #contacts = ['YourAddress@gmail.com', 'test@example.com','chebxdesigners@gmail.com']
    msg = EmailMessage()
    msg['Subject'] = "Your user " +userName+ " with email ! "+userEmail + " requested Trading Token"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'luckiusevodius@gmail.com'
    msg.set_content('The generated token for '+ userEmail + " was "+ userToken +" please send them a token and they can start using your Bot")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("email sent")








@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        userToken = secrets.token_hex(5)
        email = email=form.email.data
        name = form.username.data
        send_email_to_admin(userToken,name,email)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,token=userToken)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        userToken = form.token.data
        #realToken = user.token
        print(user.token)
        if user and ((user.token) == userToken):
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                db.session.commit()
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            flash('Wrong email or token. Please Contact peakfx to get your token', 'danger')
    return render_template('login.html', title='Login', form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route("/new_message", methods=['GET', 'POST'])
def new_message():
    if request.method == "POST":
        message = Messages(names=request.form['name'],emails=request.form['email'],subjects=request.form['subject'],messages=request.form['message'])
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
    return redirect(url_for('contact'))




@application.route("/new_call", methods=['GET', 'POST'])
def new_call():
    if request.method == "POST":
        message = Phonecall(names=request.form['author'],emails=request.form['email0'],phones=request.form['phone'])
        db.session.add(message)
        db.session.commit()
        flash('Your request was successful!', 'success')
    return redirect(url_for('index'))



@application.route("/emails", methods=['GET', 'POST'])
def emails():
    if request.method == "POST":
        message = Emails(emails=request.form['ss'])
        db.session.add(message)
        db.session.commit()
        flash('Your request was successful!', 'success')
    return redirect(url_for('index'))




@application.route("/get_message")
def get_message():
    allmessages = Messages.query.all()
    return render_template('get_message.html',allmessages=allmessages)



@application.route("/get_call")
def get_call():
    allcalls = Phonecall.query.all()
    return render_template('get_call.html',allcalls=allcalls)



@application.route("/get_email")
def get_email():
    allemails = Emails.query.all()
    return render_template('get_emails.html',allemails=allemails)




# Uploads settings the config that not taken into a init.py file
application.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + 'static/profile_pics'
photos = UploadSet('photos', IMAGES)
configure_uploads(application, photos)
patch_request_class(application)  # set maximum file size, default is 16MB
photos = UploadSet('photos', IMAGES)



class Profesionalform(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'),FileRequired(u'File was empty!')])
    submit = SubmitField(u'Submit')





@application.route('/profesional_fill', methods=['GET', 'POST'])
def profesional_fill():
    form = Profesionalform()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        new_file = file_url
        print(new_file)
        message = Profesional(title=form.title.data,content=form.content.data,author=current_user,image_file=new_file)
        db.session.add(message)
        db.session.commit()
        flash('Your profile has been created!', 'success')
        return redirect(url_for('profesional_fill'))
    else:
        file_url = None
    return render_template('post.html', form=form)





@application.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
#@login_required
def delete_post(post_id):
    post = Profesional.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted! Create a new one', 'success')
    return redirect(url_for('profesional_fill'))



if __name__ == '__main__':
    #application.debug = True
    application.run()


#ns37.domaincontrol.com
#ns38.domaincontrol.com

#amanda.ns.cloudflare.com
#dean.ns.cloudflare.com