import json
import requests
from requests.auth import HTTPBasicAuth
from flask import jsonify
from api_1_0 import api, errors, rabbitmq_params


@api.route('/')
def index():
    return 'API v1'


@api.route('metrics/queues/<string:vhost_name>/<string:queue_name>', methods=['GET'])
def get_queue_metrics(vhost_name: str, queue_name: str):
    """
    Get queue metrics from RabbitMQ API
    :param vhost_name: name of RabbitMQ vhost
    :param queue_name: name of RabbitMQ queue
    :return: metrics in json format
    """
    url = f"http://{rabbitmq_params['host']}:{rabbitmq_params['port']}/api/" \
          f"queues/{vhost_name}/{queue_name}"

    response = requests.get(url, auth=HTTPBasicAuth(rabbitmq_params['login'],
                                                    rabbitmq_params['password']))
    json_response = json.loads(response.text)

    if json_response.get('error'):
        message = f"Can't find metrics for queue {queue_name} at vhost {vhost_name}"
        return errors.not_found(message)

    else:
        return jsonify({
            'consumers': json_response['consumers'],
            'messages': json_response['messages'],
            'messages_ready': json_response['messages_ready'],
            'messages_unacknowledged': json_response['messages_unacknowledged'],
        })
