import pika
import pika.exceptions
from utils.logger import logger

RABBITMQ_HOST = '192.168.99.106'
RABBITMQ_PORT = 32037
RABBITMQ_LOGIN = 'QW5uCWWkLdEkiWcHcLl1vLB-VgjYL0at'
RABBITMQ_PASS = 'XFr5TnE55Nnn_dM6YpecoCykVnjSXiz7'
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_QUEUE = 'person_queue'


def main():

    connection = None

    try:
        credentials = pika.PlainCredentials(RABBITMQ_LOGIN, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                                       port=RABBITMQ_PORT,
                                                                       virtual_host=RABBITMQ_VIRTUAL_HOST,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(RABBITMQ_QUEUE)

        channel.basic_consume(RABBITMQ_QUEUE, callback, auto_ack=True)
        channel.start_consuming()

    except Exception as pika_ex:
        logger.warning(pika_ex)

    finally:
        connection.close()


def callback(ch, method, properties, body):
    logger.info(body)


if __name__ == '__main__':

    try:
        logger.info('Consumer application started')
        main()

    except Exception as exception:
        logger.warning(exception)

    finally:
        logger.info('Consumer application stopped')
