import os
from flask import Flask
from utils.logger import logger
from main import main as main_blueprint
from api_1_0 import api as api_1_0_blueprint


def main():

    # Web-server environment variables
    server_params = {
        'host': os.environ['SERVER_HOST'],
        'port': os.environ['SERVER_PORT']
    }

    # Config Flask app
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    # Run Flask web-server
    app.run(debug=True, host=server_params['host'], port=server_params['port'])


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as e:
        logger.critical(e)
