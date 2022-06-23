from flask import Flask, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_authorize import Authorize
from config import config
import psycopg2
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger()

db = SQLAlchemy()

def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')
    
    db.init_app(app)
    

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from App.models.user import User

    admin = Admin(app, name='control Panel')
    admin.add_view(ModelView(User, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from App.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from App.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # from App.routes.article import article as article_blueprint
    # app.register_blueprint(article_blueprint)
    
    return app

app = create_app()
db.drop_all(app=create_app())
db.create_all(app=create_app())



@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return render_template('error.html')


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return render_template('error.html')


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return render_template('error.html')


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return render_template('error.html')