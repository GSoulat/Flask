from flask import Blueprint, render_template
from flask_login import login_required, current_user
from App.models.user import User
from App import db

main = Blueprint('main',__name__, static_folder='/App/static', template_folder='App/templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():    
    return render_template('profile.html', profil=current_user)


@main.route('/list_users')
def list_users():
    print(current_user.name)
    list_user = db.session.query(User).all()
    print(list_user)
    return render_template('list_users.html', name=list_user)