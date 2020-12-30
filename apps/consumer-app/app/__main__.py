import os
from receiver import Receiver
from rabbitmq.client import Client
from utils.logger import logger


def main():

    # Environment variables
    host = os.environ['RABBITMQ_HOST']
    port = int(os.environ['RABBITMQ_PORT'])
    virtual_host = os.environ['RABBITMQ_VIRTUAL_HOST']
    login = os.environ['RABBITMQ_LOGIN']
    password = os.environ['RABBITMQ_PASS']
    exchange_name = os.environ['RABBITMQ_EXCHANGE_NAME']
    exchange_type = os.environ['RABBITMQ_EXCHANGE_TYPE']
    queue = os.environ['RABBITMQ_QUEUE']

    # Receiver settings
    client = Client(host, port, virtual_host, login, password)
    receiver = Receiver(client, process, exchange_name, exchange_type, queue)
    receiver.subscribe()


def process(data):
    logger.info(data)


if __name__ == '__main__':

    try:
        logger.info('Consumer application started')
        main()

    except Exception as e:
        logger.critical(e)
