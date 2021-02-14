import json
from abc import ABC
from utils.rabbit_manager import RabbitManager


class Consumer(RabbitManager, ABC):
    """
    RabbitMQ data consumer
    Get data exchange
    """
    def __init__(self, params: dict, function):
        """
        :param params: RabbitMQ client params
        :param function: external processing function
        """
        super().__init__(params)
        self._queue_name = params['queue_name']
        self._function = function
        self._set()

    @RabbitManager._reconnect_exception
    def _set(self):
        """
        Set channel configuration
        """
        self._client.channel.exchange_declare(exchange=self._exchange_name,
                                              exchange_type=self._exchange_type,
                                              durable=True)
        self._client.channel.queue_declare(queue=self._queue_name, durable=True)
        self._client.channel.queue_bind(exchange=self._exchange_name, queue=self._queue_name)
        self._client.channel.basic_qos(prefetch_count=1)
        self._client.channel.basic_consume(queue=self._queue_name,
                                           on_message_callback=self._callback)

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

    @RabbitManager._reconnect_exception
    def run(self):
        """
        Main function
        """
        self._client.channel.start_consuming()
