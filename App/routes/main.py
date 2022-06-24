from flask import Blueprint, render_template
from flask_login import login_required, current_user
from App.models.user import User
from App import db
import logging as lg
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

main = Blueprint('main',__name__, static_folder='/App/static', template_folder='App/templates')

config_integration.trace_integrations(['logging'])
logger = lg.getLogger(__name__)

handler = AzureLogHandler(connection_string='InstrumentationKey=711ef30c-34e7-4826-911e-57e2a5870ffa')
handler.setFormatter(lg.Formatter('%(spanId)s %(message)s'))
logger.addHandler(handler)

tracer = Tracer(
    exporter=AzureExporter(connection_string='InstrumentationKey=711ef30c-34e7-4826-911e-57e2a5870ffa'),
    sampler=ProbabilitySampler(1.0)
)

@main.route('/')
def index():
    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')
    return render_template('index.html')


@main.route('/profile')
def profile():
    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')    
    return render_template('profile.html', profil=current_user)


@main.route('/list_users')
def list_users():
    print(current_user.name)
    list_user = db.session.query(User).all()
    print(list_user)
    logger.warning('Before the span')
    with tracer.span(name='test'):
        logger.warning('In the span')
    logger.warning('After the span')
    return render_template('list_users.html', name=list_user)