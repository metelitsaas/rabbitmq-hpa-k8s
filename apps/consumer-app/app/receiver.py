import json
from rabbitmq.client import Client


class Receiver:
    """
    RabbitMQ data receiver
    Get data exchange
    """
    def __init__(self, client: Client, function, exchange_name: str, exchange_type: str, queue: str):
        """
        :param client: RabbitMQ client
        :param function: external processing function
        :param exchange_name: name of exchange
        :param exchange_type: type of exchange
        :param queue: name of queue
        """
        self._channel = client.get_channel()
        self._function = function
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue = queue
        self._set()

    def _set(self):
        """
        Set receiver configuration
        """
        self._channel \
            .exchange_declare(self._exchange_name, self._exchange_type) \
            .queue_declare(self._queue) \
            .queue_bind(self._exchange_name, self._queue) \
            .basic_qos() \
            .basic_consume(self._queue, self._callback)

    def _callback(self, ch, method, properties, body):
        """
        Send to external processing function
        :param ch:
        :param method:
        :param properties:
        :param body:
        """
        data = json.loads(body)
        self._function(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def subscribe(self):
        """
        Get data function
        """
        self._channel.subscribe()
