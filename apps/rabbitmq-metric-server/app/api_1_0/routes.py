import json
import requests
import datetime
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from flask import jsonify
from api_1_0 import api, errors, rabbitmq_params


@api.route('/')
def index():
    """
    API index response
    """
    return jsonify({'apiVersion': '/v1beta1'})


@api.route('namespaces/<string:namespace>/services/<string:service_name>/'
           '<string:queue_name>_<string:metric_name>', methods=['GET'])
def get_queue_metric(namespace: str, service_name: str, queue_name: str, metric_name: str):
    """
    Get queue metrics from RabbitMQ API
    :param namespace: metric server namespace
    :param service_name: metric server name
    :param queue_name: name of RabbitMQ queue
    :param metric_name: name of RabbitMQ queue's metric
    :return: metrics in json format
    """
    url = f"http://{rabbitmq_params['host']}:{rabbitmq_params['port']}/api/" \
          f"queues/{rabbitmq_params['vhost']}/{queue_name}"

    try:
        response = requests.get(url, auth=HTTPBasicAuth(rabbitmq_params['login'],
                                                        rabbitmq_params['password']))
        json_response = json.loads(response.text)

        if not json_response.get(f'{metric_name}'):
            raise ValueError

        return jsonify({
            'kind': 'MetricValueList',
            'apiVersion': 'custom.metrics.k8s.io/v1beta1',
            'metadata': {
                'selfLink': '/apis/custom.metrics.k8s.io/v1beta1/'
            },
            'items': [
                {
                    'describedObject': {
                        'kind': 'Service',
                        'namespace': f'{namespace}',
                        'name': f'{service_name}',
                        'apiVersion': '/v1beta1'
                    },
                    'metricName': f'{queue_name}_{metric_name}',
                    'timestamp': datetime.datetime.now().astimezone().isoformat(),
                    'value': json_response[f'{metric_name}']
                }
            ]
        })

    except ValueError:
        message = f"Can't find metric {metric_name} for queue {queue_name} " \
                  f"at vhost {rabbitmq_params['vhost']}"
        return errors.not_found(message)

    except ConnectionError:
        message = f"Connection error at url: {url}"
        return errors.not_found(message)
