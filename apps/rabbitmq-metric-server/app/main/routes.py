from main import main


@main.route('/')
def index():
    return 'RabbitMQ Metric Server'
