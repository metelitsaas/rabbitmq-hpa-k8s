import os
from receiver import Receiver
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

    # Receiver settings
    receiver = Receiver(connection_params, process)
    receiver.subscribe()


def process(data):
    logger.info(data)


if __name__ == '__main__':

    try:
        logger.info('Consumer application started')
        main()

    except Exception as e:
        logger.critical(e)
