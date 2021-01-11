import sys
import time
import pika
from pika.exceptions import AMQPConnectionError
from rabbitmq.channel import Channel
from utils.logger import logger

RECONNECT_ATTEMPTS = 10
RECONNECT_PERIOD = 1


class SingletonMeta(type):
    """
    Singleton class realization
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Client(metaclass=SingletonMeta):
    """
    RabbitMQ client, realized as singleton
    """
    def __init__(self, host: str, port: str, virtual_host: str, login: str, password: str):
        """
        :param host: RabbitMQ hostname
        :param port: RabbitMQ port
        :param virtual_host: RabbitMQ virtual host
        :param login: RabbitMQ login
        :param password: RabbitMQ password
        """
        self._host = host
        self._port = int(port)
        self._virtual_host = virtual_host
        self._credentials = pika.PlainCredentials(login, password)
        self._connection_params = pika.ConnectionParameters(host=self._host,
                                                            port=self._port,
                                                            virtual_host=self._virtual_host,
                                                            credentials=self._credentials)
        self.connection = None
        self.connect()

    def connect(self) -> pika.connection:
        """
        Connect to RabbitMQ instance
        Reconnect number of attempts if disconnected, otherwise exit
        :return: RabbitMQ connection
        """
        for attempt in range(RECONNECT_ATTEMPTS):

            try:
                logger.info(f'Connecting to {self._host}:{self._port}')
                self.connection = pika.BlockingConnection(self._connection_params)
                logger.info(f'Connected')
                return

            except AMQPConnectionError:
                logger.warning(f'Unable to connect, reconnect attempt: {attempt}')
                time.sleep(RECONNECT_PERIOD)

        # Handle exit from program
        logger.critical('Unable to connect, signal to exit')
        self.connection.close()
        sys.exit()

    def get_channel(self) -> Channel:
        """
        Get channel from current connection
        :return: RabbitMQ channel
        """
        logger.info('Creating channel')
        return Channel(self)
