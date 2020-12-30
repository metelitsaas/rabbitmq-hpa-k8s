class Loader:
    def __init__(self, client, exchange_name, exchange_type):
        self._channel = client.get_channel()
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._set()

    def _set(self):
        self._channel.exchange_declare(self._exchange_name, self._exchange_type)

    def load(self, data):
        self._channel.publish(data, self._exchange_name)
