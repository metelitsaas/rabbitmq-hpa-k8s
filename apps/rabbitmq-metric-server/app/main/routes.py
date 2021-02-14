from flask import jsonify
from main import main


@main.route('/')
def index():
    """
    Root index response
    """
    return 'RabbitMQ Metric Server'


@main.route('/status')
def get_status():
    """
    Check web-server liveness
    """
    return jsonify({'status': 'healthy'})
