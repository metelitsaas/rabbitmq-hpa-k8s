import os
from flask import Blueprint

api = Blueprint('api_1_0', __name__)

# RabbiMQ environment variables
rabbitmq_params = {
    'host': os.environ['RABBITMQ_HOST'],
    'port': os.environ['RABBITMQ_PORT'],
    'login': os.environ['RABBITMQ_LOGIN'],
    'password': os.environ['RABBITMQ_PASS'],
    'vhost': os.environ['RABBITMQ_VHOST']
}

from api_1_0 import errors, routes
