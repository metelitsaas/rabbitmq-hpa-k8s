import json
from abc import ABC
import pika
from utils.rabbit_manager import RabbitManager


class Producer(RabbitManager, ABC):
    """
    RabbitMQ data producer
    Publish to exchange
    """
    def __init__(self, params: dict):
        """
        :param params: RabbitMQ client params
        """
        super().__init__(params)
        self._set()

    @RabbitManager._reconnect_exception
    def _set(self) -> None:
        """
        Set channel configuration
        """
        self._client.channel.exchange_declare(exchange=self._exchange_name,
                                              exchange_type=self._exchange_type,
                                              durable=True)

    @RabbitManager._reconnect_exception
    def _send_message(self, data: dict) -> None:
        """
        Encode message and send to broker
        :param data: data to load
        """
        message = json.dumps(data, default=self._datetime_handler).encode()
        self._client.channel.basic_publish(
                    exchange=self._exchange_name,
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
