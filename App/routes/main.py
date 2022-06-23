from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main',__name__, static_folder='/App/static', template_folder='App/templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    print(current_user.name)
    
    return render_template('profile.html', name=current_user.name)


@main.route('/list_users')
def list_users():
    print(current_user.name)
    
    return render_template('profile.html', name=current_user.name)