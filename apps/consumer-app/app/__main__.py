import time
import random
import json
import pika
import pika.exceptions
from utils.logger import logger

UPDATE_PERIOD = 3  # second

RABBITMQ_HOST = '192.168.99.107'
RABBITMQ_PORT = 30999
RABBITMQ_LOGIN = 'FCv8IRXQVICBfUupdMsBOxk71o7JKd2r'
RABBITMQ_PASS = 'mWsrsUhzhH1EH57Sze6DxWpX64cGqNvB'
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_QUEUE = 'person_durable_queue'


def main():

    connection = None

    try:
        # Create connection
        credentials = pika.PlainCredentials(RABBITMQ_LOGIN, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                                       port=RABBITMQ_PORT,
                                                                       virtual_host=RABBITMQ_VIRTUAL_HOST,
                                                                       credentials=credentials))
        # Define channel
        channel = connection.channel()

        # Define exchange
        channel.exchange_declare(exchange='direct_logs',
                                 exchange_type='direct')

        # Define queue
        result = channel.queue_declare(queue='', exclusive=True)  # Create durable queue with dynamic name
        queue_name = result.method.queue

        # Define bind
        #channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='info')
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='error')

        # Consume messages from queue
        channel.basic_qos(prefetch_count=1)  # receive only one message until confirm acknowledge
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except Exception as pika_ex:
        logger.warning(pika_ex)

    finally:
        connection.close()


def callback(ch, method, properties, body):
    # Latency simulation
    time.sleep(random.randrange(UPDATE_PERIOD))
    logger.info(json.loads(body))


if __name__ == '__main__':

    try:
        logger.info('Consumer application started')
        main()

    except Exception as exception:
        logger.warning(exception)

    finally:
        logger.info('Consumer application stopped')
