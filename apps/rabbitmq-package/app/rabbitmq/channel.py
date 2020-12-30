import pika
from pika.exceptions import StreamLostError, ConnectionClosedByBroker
from functools import wraps
from rabbitmq.client import Client
from utils.logger import logger


class Channel:
    """
    RabbitMQ channel
    """
    def __init__(self, client: Client):
        """
        :param client: RabbitMQ client
        """
        self._client = client
        self._channel = client.connection.channel()

    class _Decorators:
        """
        Decorator class for exceptions
        """
        @classmethod
        def reconnect_exception(cls, function):
            """
            Reconnect if exception raised
            :param function: function to be wrapped
            :return: wrapped function
            """
            @wraps(function)
            def wrapper(self, *method_args, **method_kwargs):
                try:
                    return function(self, *method_args, **method_kwargs)
                except (StreamLostError, ConnectionClosedByBroker) as e:
                    logger.warning(e)
                    self._client.connect()

            return wrapper

    @_Decorators.reconnect_exception
    def exchange_declare(self, exchange_name: str, exchange_type: str):
        """
        Declare exchange
        :param exchange_name: name of exchange
        :param exchange_type: type of exchange
        :return: RabbitMQ channel
        """
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=exchange_type)

        return self

    @_Decorators.reconnect_exception
    def queue_declare(self, queue):
        """
        Declare queue
        :param queue: name of queue
        :return: RabbitMQ channel
        """
        self._channel.queue_declare(queue=queue, durable=True)

        return self

    @_Decorators.reconnect_exception
    def queue_bind(self, exchange_name, queue):
        """
        Declare binding
        :param exchange_name: name of exchange
        :param queue: name of queue
        :return: RabbitMQ channel
        """
        self._channel.queue_bind(exchange=exchange_name, queue=queue)

        return self

    @_Decorators.reconnect_exception
    def basic_qos(self):
        """
        Declare channel prefetch mechanism
        :return: RabbitMQ channel
        """
        self._channel.basic_qos(prefetch_count=1)

        return self

    @_Decorators.reconnect_exception
    def basic_consume(self, queue, callback):
        """
        Declare consumer
        :param queue: name of queue
        :param callback: callback function
        :return: RabbitMQ channel
        """
        self._channel.basic_consume(queue=queue, on_message_callback=callback)

        return self

    @_Decorators.reconnect_exception
    def publish(self, data, exchange_name):
        """
        Publish data to exchange
        :param data: data to publish
        :param exchange_name: name of exchange
        """
        self._channel.basic_publish(exchange=exchange_name,
                                    routing_key='',
                                    body=data,  # Serialized data
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # Make message persistent
                                    ))

    @_Decorators.reconnect_exception
    def subscribe(self):
        """
        Subscribe data from channel
        """
        self._channel.start_consuming()
