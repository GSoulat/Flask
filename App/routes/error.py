from amqp import NotFound
from flask import Blueprint, jsonify, render_template

error_bp = Blueprint('error_bp', __name__, static_folder='/App/static', template_folder='App/templates')



@error_bp.app_errorhandler(NotFound)
def handle_generic_exception(err):
    return jsonify({'messsaes': "This ressources isn't available."}), 404

@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    return render_template('error.html', err=err), 500

