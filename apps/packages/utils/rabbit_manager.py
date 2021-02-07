from abc import ABCMeta, abstractmethod
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
                self.set()

    return wrapper


class RabbitManager(metaclass=ABCMeta):
    """
    Abstract class of RabbitMQ producer/consumer
    """
    def __init__(self, params: dict):
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
        self.set()

    @abstractmethod
    def set(self) -> None:
        """
        Set channel configuration
        """
