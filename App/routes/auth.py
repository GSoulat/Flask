from flask import Blueprint, redirect, render_template, session, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from App.models.user import User
from App import db
import re
# import cloudinary.uploader


auth = Blueprint('auth', __name__, static_folder='/App/static', template_folder='App/templates')

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    if(re.fullmatch(regex, email)):
        print("Valid Email")
        print(email)
    else:
        print("Invalid Email")
        flash('Email is not a email adress.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    print('----------------------------------------------')
    print(user)
    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    print('----------------------------------------------')

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    work = request.form.get('lastname')
    github = request.form.get('password')

    if(re.fullmatch(regex, email)):
        print("Valid Email")
    else:
        print("Invalid Email")
        flash('Email is not a email adress.')
        return redirect(url_for('auth.signup'))
    
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))
    
    #   file_to_upload = request.files.get('profil')
    #     if file_to_upload:
    #         print('file to upload')
    #         upload_result = cloudinary.uploader.upload(file_to_upload)
    #         app.logger.info(upload_result)
    #         current_user.filename = upload_result['secure_url']


    new_user = User(email=email, firstname=firstname,lastname=lastname, work=work, github=github, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/callback')
def callback():
    pass


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper