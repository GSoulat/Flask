"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, session, url_for, request, flash, abort, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from App.models.user import User
from App import db, login_manager, logger, tracer, flow, GOOGLE_CLIENT_ID
import re, os
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
# import cloudinary.uploader


auth = Blueprint('auth', __name__, static_folder='/App/static', template_folder='App/templates')

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@auth.route('/googlelogin')
def googlelogin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# @auth.route('/authorize/google')
# def google_authorize():
#     google = oauth.create_client('google')
#     token = google.authorize_access_token()
#     resp = google.get('userinfo').json()
    
#     print(google)
#     print(token)
#     print(resp)           
#     return redirect('/profile')


@auth.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    user = User.query.filter_by(email=id_info.get("email")).first()
    login_user(user)
    
    return redirect(url_for("main.profile"))

@auth.route('/login',  methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    
    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if(re.fullmatch(regex, email)):
            user = User.query.filter_by(email=email).first()
        else:
            flash('Email is not a email adress.')
            return render_template('login.html')
        
        
        print(user.password_hash)
        print(password)
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            return redirect(url_for("main.profile"))
        flash("Invalid username/password combination")
        return render_template('login.html')
  

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')
        # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    
    if request.method == "GET":
        return render_template('signup.html')
    
    if request.method == "POST":
    
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        work = request.form.get('work')
        github = request.form.get('github')

        if(re.fullmatch(regex, email)):
            user = User.query.filter_by(email=email).first()
        else:
            flash('Email is not a email adress.')
            return redirect(url_for('auth.signup'))

        if user:
            flash('Email address already exists.')
            return redirect(url_for('auth.signup'))
        
        #   file_to_upload = request.files.get('profil')
        #     if file_to_upload:
        #         print('file to upload')
        #         upload_result = cloudinary.uploader.upload(file_to_upload)
        #         app.logger.info(upload_result)
        #         current_user.filename = upload_result['secure_url']


        new_user = User(email=email, firstname=firstname,lastname=lastname, work=work, github=github, password_hash=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login"))

    
