from flask import Flask, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_authorize import Authorize
from config import config
# from flask_mail import Mail
# import cloudinary
import psycopg2
import logging as lg
import os
from applicationinsights.flask.ext import AppInsights

lg.basicConfig(level=lg.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[lg.StreamHandler(), lg.FileHandler(filename='error.log')])

logger = lg.getLogger()

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
    
    from App.routes.error import error_bp as error_blueprint
    app.register_blueprint(error_blueprint)
    
    # from App.routes.article import article as article_blueprint
    # app.register_blueprint(article_blueprint)
    
    
    # app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    # app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_PORT'] = 465
    # mail = Mail(app)
    
    # cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    # api_secret=os.getenv('API_SECRET'))
    

    
    return app

app = create_app()

# lg.warning('Database start to initialize')
# db.drop_all(app=create_app())
# db.create_all(app=create_app())
# lg.warning('Database created successfully')

# @app.errorhandler(400)
# def handle_400_error(_error):
#     """Return a http 400 error to client"""
#     return render_template('error.html')


# @app.errorhandler(401)
# def handle_401_error(_error):
#     """Return a http 401 error to client"""
#     return render_template('error.html')


# @app.errorhandler(404)
# def handle_404_error(_error):
#     """Return a http 404 error to client"""
#     return render_template('error.html')


# @app.errorhandler(500)
# def handle_500_error(_error):
#     """Return a http 500 error to client"""
#     return render_template('error.html')


appinsights = AppInsights(app)

@app.after_request
def after_request(response):
    appinsights.flush()
    return response

@app.route("/coco")
def hello():
    app.logger.debug('This is a debug log message')
    app.logger.info('This is an information log message')
    app.logger.warn('This is a warning log message')
    app.logger.error('This is an error message')
    app.logger.critical('This is a critical message')
    return "Hello World!"


from logging import StreamHandler

# keep stdout/stderr logging using StreamHandler
streamHandler = StreamHandler()
app.logger.addHandler(streamHandler)


# after Application Insights configuration

# keep stdout/stderr logging using StreamHandler
streamHandler = StreamHandler()
app.logger.addHandler(streamHandler)

# define log level to DEBUG
app.logger.setLevel(lg.DEBUG)

# apply same formatter on all log handlers
for logHandler in app.logger.handlers:
  logHandler.setFormatter(lg.Formatter('[FLASK-SAMPLE][%(levelname)s]%(message)s'))