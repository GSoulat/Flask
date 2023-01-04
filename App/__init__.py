from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# import google.auth.transport.requests
import os
from datetime import timedelta
from config import config
# from flask_mail import Mail
# import cloudinary
import psycopg2
from logging import StreamHandler
import os
from applicationinsights.flask.ext import AppInsights
import logging as lg
# from opencensus.ext.azure.log_exporter import AzureLogHandler
# from opencensus.ext.azure.trace_exporter import AzureExporter
# from opencensus.trace import config_integration
# from opencensus.trace.samplers import ProbabilitySampler
# from opencensus.trace.tracer import Tracer
# import pathlib

lg.basicConfig(level=lg.DEBUG,
                   format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                   datefmt='%Y-%m-%d %H:%M:%S',
                   handlers=[lg.StreamHandler(), lg.FileHandler(filename='error.log')])

# config_integration.trace_integrations(['logging'])
logger = lg.getLogger(__name__)

# handler = AzureLogHandler(connection_string='InstrumentationKey=' + os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY'))
# handler.setFormatter(lg.Formatter('%(spanId)s %(message)s'))
# logger.addHandler(handler)

# tracer = Tracer(
#     exporter=AzureExporter(connection_string='InstrumentationKey='+ os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')),
#     sampler=ProbabilitySampler(1.0)
# )

db = SQLAlchemy()
login_manager = LoginManager()

# GOOGLE_CLIENT_ID = "54816233296-p388b2tfmotc18r9166t06umnmmbaua9.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
#     redirect_uri="http://127.0.0.1:8000/callback"
# )
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def create_app():
    logger.info(f'Starting app in {config.APP_ENV} environment')
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    db.init_app(app)
    
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from App.models.user import User

    from App.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from App.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from App.routes.error import error_bp as error_blueprint
    app.register_blueprint(error_blueprint)


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


# @app.cli.command("init_db")
# def init_db():
#     models.init_db()

# lg.warning('Database start to initialize')
# db.drop_all(app=create_app())
# db.create_all(app=create_app())
# lg.warning('Database created successfully')

# appinsights = AppInsights(app)

# @app.after_request
# def after_request(response):
#     appinsights.flush()
#     return response

# # keep stdout/stderr logging using StreamHandler
# streamHandler = StreamHandler()
# app.logger.addHandler(streamHandler)
# # after Application Insights configuration

# # keep stdout/stderr logging using StreamHandler
# streamHandler = StreamHandler()
# app.logger.addHandler(streamHandler)

# # define log level to DEBUG
# app.logger.setLevel(lg.WARN)

# # apply same formatter on all log handlers
# for logHandler in app.logger.handlers:
#   logHandler.setFormatter(lg.Formatter('[FLASK-LOG][%(levelname)s]%(message)s'))
  
# @app.route("/coco")
# def hello():
#     app.logger.debug('This is a debug log message')
#     app.logger.info('This is an information log message')
#     app.logger.warn('This is a warning log message')
#     app.logger.error('This is an error message')
#     app.logger.critical('This is a critical message')
#     return "Hello World!"