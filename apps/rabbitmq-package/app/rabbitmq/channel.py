import pika
from pika.exceptions import StreamLostError, ConnectionClosedByBroker
from functools import wraps
from utils.logger import logger


class Channel:
    def __init__(self, client):
        self._client = client
        self._channel = client.connection.channel()

    class _Decorators:
        @classmethod
        def reconnect_exception(cls, function):
            @wraps(function)
            def wrapper(self, *method_args, **method_kwargs):
                try:
                    return function(self, *method_args, **method_kwargs)
                except (StreamLostError, ConnectionClosedByBroker) as e:
                    logger.warning(e)
                    self._client.connect()

            return wrapper

    @_Decorators.reconnect_exception
    def exchange_declare(self, exchange_name, exchange_type):
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=exchange_type)

        return self

    @_Decorators.reconnect_exception
    def queue_declare(self, queue):
        self._channel.queue_declare(queue=queue, durable=True)

        return self

    @_Decorators.reconnect_exception
    def queue_bind(self, exchange_name, queue):
        self._channel.queue_bind(exchange=exchange_name, queue=queue)

        return self

    @_Decorators.reconnect_exception
    def basic_qos(self):
        self._channel.basic_qos(prefetch_count=1)

        return self

    @_Decorators.reconnect_exception
    def basic_consume(self, queue, callback):
        self._channel.basic_consume(queue=queue, on_message_callback=callback)

        return self

    @_Decorators.reconnect_exception
    def publish(self, data, exchange_name):
        self._channel.basic_publish(exchange=exchange_name,
                                    routing_key='',
                                    body=data,  # Serialized data
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # Make message persistent
                                    ))

    @_Decorators.reconnect_exception
    def subscribe(self):
        self._channel.start_consuming()
