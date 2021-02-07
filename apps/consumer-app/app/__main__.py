import os
from consumer import Consumer
from utils.logger import logger


def main():

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
    logger.info(data)


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as e:
        logger.critical(e)
