import os
import time
from consumer import Consumer
from utils.logger import logger

PROCESSING_LAG_SEC = 2


def main():
    """ Main consumer-app function"""

    # Environment variables
    connection_params = {
        'host': os.environ['RABBITMQ_HOST'],
        'port': os.environ['RABBITMQ_PORT'],
        'vhost': os.environ['RABBITMQ_VHOST'],
        'login': os.environ['RABBITMQ_LOGIN'],
        'password': os.environ['RABBITMQ_PASS'],
        'exchange_name': os.environ['RABBITMQ_EXCHANGE_NAME'],
        'exchange_type': os.environ['RABBITMQ_EXCHANGE_TYPE'],
        'queue_name': os.environ['RABBITMQ_QUEUE']
    }

    # Consumer settings
    consumer = Consumer(connection_params, process)
    consumer.run()


def process(data):
    """
    Data processing function
    :param data: received data
    """
    logger.info(data)
    time.sleep(PROCESSING_LAG_SEC)


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as exception:
        logger.exception(exception)
        logger.critical('Critical exception')
