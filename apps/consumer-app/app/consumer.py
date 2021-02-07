import json
from abc import ABC
from utils.rabbit_manager import RabbitManager, reconnect_exception


class Consumer(RabbitManager, ABC):
    """
    RabbitMQ data consumer
    Get data exchange
    """
    def __init__(self, params, function):
        """
        :param params: RabbitMQ client params
        :param function: external processing function
        """
        self._rabbit_exchange_name = params['exchange_name']
        self._rabbit_exchange_type = params['exchange_type']
        self._rabbit_queue_name = params['queue_name']
        self._function = function
        super().__init__(params)

    @reconnect_exception
    def set(self):
        """
        Set channel configuration
        """
        self.rabbit_client.channel \
            .exchange_declare(exchange=self._rabbit_exchange_name,
                              exchange_type=self._rabbit_exchange_type,
                              durable=True)
        self.rabbit_client.channel.queue_declare(queue=self._rabbit_queue_name, durable=True)
        self.rabbit_client.channel.queue_bind(exchange=self._rabbit_exchange_name,
                                              queue=self._rabbit_queue_name)
        self.rabbit_client.channel.basic_qos(prefetch_count=1)
        self.rabbit_client.channel.basic_consume(queue=self._rabbit_queue_name,
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

    @reconnect_exception
    def run(self):
        """
        Main function
        """
        self.rabbit_client.channel.start_consuming()
