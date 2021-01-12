import os
import time
import random
import json
from utils.logger import logger
from rabbitmq.client import Client
from loader import Loader
from functions import *


def main():

    # Environment variables
    update_period = int(os.environ['UPDATE_PERIOD'])
    host = os.environ['RABBITMQ_HOST']
    port = os.environ['RABBITMQ_PORT']
    virtual_host = os.environ['RABBITMQ_VIRTUAL_HOST']
    login = os.environ['RABBITMQ_LOGIN']
    password = os.environ['RABBITMQ_PASS']
    exchange_name = os.environ['RABBITMQ_EXCHANGE_NAME']
    exchange_type = os.environ['RABBITMQ_EXCHANGE_TYPE']

    # Loader settings
    client = Client(host, port, virtual_host, login, password)
    people_loader = Loader(client, exchange_name, exchange_type)

    # Produce messages in loop with latency
    counter = 1
    while True:
        # Data generation
        message = generate_fake_data()
        data = {
            'id': counter,
            'message': message
        }

        # Serialize and send data
        serialized_data = json.dumps(data)
        people_loader.load(serialized_data)

        # Increment counter and wait for new iteration
        counter += 1
        logger.info(data)
        time.sleep(random.randrange(update_period))


if __name__ == '__main__':

    try:
        logger.info('Producer application started')
        main()

    except Exception as e:
        logger.critical(e)
