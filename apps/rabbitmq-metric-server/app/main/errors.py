from flask import make_response, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(error):
    """
    Handling 404 status error
    :param error: error message
    :return: json error message
    """
    response = jsonify({'error': 'page_not_found'})
    status_code = 404
    return make_response(response, status_code)


@main.app_errorhandler(500)
def internal_server_error(error):
    """
    Handling 500 status error
    :param error: error message
    :return: json error message
    """
    response = jsonify({'error': 'internal_server_error'})
    status_code = 500
    return make_response(response, status_code)
