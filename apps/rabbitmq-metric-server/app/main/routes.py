from main import main


@main.route('/')
def index():
    """
    Root index response
    """
    return 'RabbitMQ Metric Server'
