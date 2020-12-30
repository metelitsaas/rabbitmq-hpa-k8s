import json


class Receiver:
    def __init__(self, client, function, exchange_name, exchange_type, queue):
        self._channel = client.get_channel()
        self._function = function
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue = queue
        self._set()

    def _set(self):
        self._channel \
            .exchange_declare(self._exchange_name, self._exchange_type) \
            .queue_declare(self._queue) \
            .queue_bind(self._exchange_name, self._queue) \
            .basic_qos() \
            .basic_consume(self._queue, self._callback)

    def _callback(self, ch, method, properties, body):
        data = json.loads(body)
        self._function(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def subscribe(self):
        self._channel.subscribe()
