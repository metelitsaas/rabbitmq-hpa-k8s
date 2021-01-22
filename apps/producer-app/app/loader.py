import json
import datetime
import pika
from pika.exceptions import StreamLostError, ConnectionClosedByBroker
from functools import wraps
from utils.logger import logger
from utils.rabbit_client import RabbitClient


def reconnect_exception(function):
    """
    Reconnect if exception raised
    :param function: wrapped function
    :return: wrapper function
    """
    @wraps(function)
    def wrapper(self, *method_args, **method_kwargs):
        while True:

            try:
                function(self, *method_args, **method_kwargs)
                break

            except (StreamLostError, ConnectionClosedByBroker) as error:
                logger.warning(error)
                self.rabbit_client.connect()

    return wrapper


class Loader:
    """
    RabbitMQ data loader
    Publish to exchange
    """
    def __init__(self, params):
        """
        :param params: RabbitMQ client params
        """
        self.rabbit_client = RabbitClient(
            params['host'],
            params['port'],
            params['vhost'],
            params['login'],
            params['password']
        )
        self._rabbit_exchange_name = params['exchange_name']
        self._rabbit_exchange_type = params['exchange_type']
        self._set()

    @staticmethod
    def _datetime_handler(value) -> str:
        """
        Wrap datatime values to ISO format
        :param value: value to check
        :return: wrapped value
        """
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return value

    @reconnect_exception
    def _set(self) -> None:
        """
        Set loader configuration
        """
        self.rabbit_client.channel.exchange_declare(exchange=self._rabbit_exchange_name,
                                                    exchange_type=self._rabbit_exchange_type,
                                                    durable=True)

    @reconnect_exception
    def _send_message(self, data: dict) -> None:
        """
        Encode message and send to broker
        :param data: data to load
        """
        message = json.dumps(data, default=self._datetime_handler).encode()
        self.rabbit_client.channel.basic_publish(
                    exchange=self._rabbit_exchange_name,
                    routing_key='',
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))

    def load(self, data: dict) -> None:
        """
        Load data to exchange
        :param data: data to load
        """
        self._send_message(data)
