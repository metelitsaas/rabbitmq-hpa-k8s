import datetime
from faker import Faker


def generate_fake_data() -> dict:
    faker = Faker()
    return {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'birth_date': faker.date_of_birth().strftime('%Y-%m-%d'),
        'address': {
            'state': faker.state(),
            'city': faker.city(),
            'street_address': faker.street_address()
        },
        'links': {
            'phone': faker.phone_number()
        },
        'job': {
            'occupation': faker.job(),
            'company': faker.company()
        },
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
