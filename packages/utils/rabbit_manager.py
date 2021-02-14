import datetime
from abc import ABCMeta, abstractmethod
from functools import wraps
from pika.exceptions import StreamLostError, ConnectionClosedByBroker
from utils.logger import logger
from utils.rabbit_client import RabbitClient


class RabbitManager(metaclass=ABCMeta):
    """
    Abstract class of RabbitMQ producer/consumer
    """
    def __init__(self, params: dict):
        """
        :param params: RabbitMQ client params
        """
        self._client = RabbitClient(
            params['host'],
            params['port'],
            params['vhost'],
            params['login'],
            params['password']
        )
        self._exchange_name = params['exchange_name']
        self._exchange_type = params['exchange_type']

    @staticmethod
    def _reconnect_exception(function):
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
                    self._client.connect()
                    self._set()

        return wrapper

    @abstractmethod
    def _set(self) -> None:
        """
        Set channel configuration
        """

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
