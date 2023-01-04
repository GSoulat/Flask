from flask import Blueprint, render_template
from flask_login import login_required, current_user
from App.models.user import User
from App import db
from App.utils import admin_required

main = Blueprint('main',__name__, static_folder='/App/static', template_folder='App/templates')



@main.route('/')
def index():
    # logger.warning('Before the span')
    # with tracer.span(name='test'):
    #     logger.warning('In the span')
    # logger.warning('After the span')
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    # logger.warning('Before the span')
    # with tracer.span(name='test'):
    #     logger.warning('In the span')
    # logger.warning('After the span')    
    return render_template('profile.html', profil=current_user)


@main.route('/list_users')
@login_required
@admin_required
def list_users():
    print(current_user.isAdmin)
    list_user = db.session.query(User).all()
    print(list_user)
    # logger.warning('Before the span')
    # with tracer.span(name='test'):
    #     logger.warning('In the span')
    # logger.warning('After the span')
    return render_template('list_users.html', name=list_user)


# @main.route('/list_users')
# @login_required
# @admin_required
# def list_users():
#     print(current_user.isAdmin)
#     list_user = db.session.query(User).all()
#     print(list_user)
#     logger.warning('Before the span')
#     with tracer.span(name='test'):
#         logger.warning('In the span')
#     logger.warning('After the span')
#     return render_template('list_users.html', name=list_user)