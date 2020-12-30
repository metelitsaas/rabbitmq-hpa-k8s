from rabbitmq.client import Client


class Loader:
    """
    RabbitMQ data loader
    Publish to exchange
    """
    def __init__(self, client: Client, exchange_name: str, exchange_type: str):
        """
        :param client: RabbitMQ client
        :param exchange_name: name of exchange
        :param exchange_type: type of exchange
        """
        self._channel = client.get_channel()
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._set()

    def _set(self):
        """
        Set loader configuration
        """
        self._channel.exchange_declare(self._exchange_name, self._exchange_type)

    def load(self, data):
        """
        Load data to exchange
        :param data: data to load
        """
        self._channel.publish(data, self._exchange_name)
