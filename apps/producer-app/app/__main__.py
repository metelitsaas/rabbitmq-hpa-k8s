import os
import time
import random
from utils.logger import logger
from producer import Producer
from functions import generate_fake_data


def main():
    """ Main producer-app function"""

    # Environment variables
    update_period = int(os.environ['UPDATE_PERIOD'])
    connection_params = {
        'host': os.environ['RABBITMQ_HOST'],
        'port': os.environ['RABBITMQ_PORT'],
        'vhost': os.environ['RABBITMQ_VHOST'],
        'login': os.environ['RABBITMQ_LOGIN'],
        'password': os.environ['RABBITMQ_PASS'],
        'exchange_name': os.environ['RABBITMQ_EXCHANGE_NAME'],
        'exchange_type': os.environ['RABBITMQ_EXCHANGE_TYPE']
    }

    # Producer settings
    producer = Producer(connection_params)

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
        producer.load(data)

        # Increment counter and wait for new iteration
        counter += 1
        logger.info(data)
        time.sleep(random.randrange(update_period))


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as exception:
        logger.exception(exception)
        logger.critical('Critical exception')
