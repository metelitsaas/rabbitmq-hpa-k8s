import sys
import time
import pika
from pika.exceptions import AMQPConnectionError, StreamLostError, ConnectionClosedByBroker
from rabbitmq.channel import Channel
from utils.logger import logger

RECONNECT_ATTEMPTS = 10
RECONNECT_PERIOD = 1


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Client(metaclass=SingletonMeta):
    def __init__(self, host, port, virtual_host, login, password):
        self._host = host
        self._port = port
        self._virtual_host = virtual_host
        self._credentials = pika.PlainCredentials(login, password)
        self._connection_params = pika.ConnectionParameters(host=self._host,
                                                            port=self._port,
                                                            virtual_host=self._virtual_host,
                                                            credentials=self._credentials)
        self.connection = self.connect()

    def connect(self):
        attempt = 0
        while attempt < RECONNECT_ATTEMPTS:

            try:
                return pika.BlockingConnection(self._connection_params)

            except AMQPConnectionError:
                attempt += 1
                logger.warning(f'Unable to connect, reconnect attempt: {attempt}')
                time.sleep(RECONNECT_PERIOD)

        # Handle exit from program
        logger.critical('Unable to connect, signal to exit')
        sys.exit()

    def get_channel(self):

        try:
            return Channel(self)

        except (StreamLostError, ConnectionClosedByBroker) as e:
            logger.warning(e)
            self.connect()
