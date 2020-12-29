import time
import random
import json
import pika
import pika.exceptions
from utils.logger import logger
from functions import *

UPDATE_PERIOD = 3  # second

RABBITMQ_HOST = '192.168.99.108'
RABBITMQ_PORT = 30470
RABBITMQ_LOGIN = '5Hfzr3GH_mYnWKJEfpgS8-Mw-uZw4dB8'
RABBITMQ_PASS = 'Va62NMDROXtki5tHnnGC--hqwe7GJeY1'
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_EXCHANGE = 'people_exchange'


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
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE,
                                 exchange_type='fanout')

        # Produce messages in loop with latency
        counter = 1
        while True:
            message = generate_fake_data()
            data = {
                'id': counter,
                'message': message
            }
            # Send messages to exchange
            channel.basic_publish(exchange=RABBITMQ_EXCHANGE,
                                  routing_key='',
                                  body=json.dumps(data),  # Serialized json
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # Make message persistent
                                  ))

            counter += 1
            logger.info(data)
            time.sleep(random.randrange(UPDATE_PERIOD))

    except Exception as pika_ex:
        logger.warning(pika_ex)

    finally:
        connection.close()


if __name__ == '__main__':

    try:
        logger.info('Producer application started')
        main()

    except Exception as exception:
        logger.warning(exception)

    finally:
        logger.info('Producer application stopped')
