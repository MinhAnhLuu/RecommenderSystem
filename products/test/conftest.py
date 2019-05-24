import pytest
import redis

from products.dependencies import REDIS_URI_KEY


@pytest.fixture
def redis_config():
    return {REDIS_URI_KEY: 'redis://localhost:6379/11'}


@pytest.fixture
def config(rabbit_config, redis_config):
    config = rabbit_config.copy()
    config.update(redis_config)
    return config


@pytest.yield_fixture
def redis_client(config):
    client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))
    yield client
    client.flushdb()


@pytest.fixture
def product():
    return {
        'id': '1',
        'title': 'Honda',
        'passenger_capacity': 7,
        'maximum_speed': 230,
        'in_stock': 11,
    }


@pytest.fixture
def create_product(redis_client, product):
    def create(**overrides):
        new_product = product.copy()
        new_product.update(**overrides)
        redis_client.hmset(
            'products:{}'.format(new_product['id']),
            new_product)
        return new_product
    return create


@pytest.fixture
def products(create_product):
    return [
        create_product(
            id='2',
            title='Yamaha',
            passenger_capacity=5,
            maximum_speed=328,
            in_stock=10,
        ),
        create_product(
            id='3',
            title='Suzuki',
            passenger_capacity=7,
            maximum_speed=335,
            in_stock=16,
        ),
        create_product(
            id='4',
            title='Toyota',
            passenger_capacity=7,
            maximum_speed=235,
            in_stock=15,
        ),
    ]
