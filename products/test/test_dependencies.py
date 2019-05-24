import pytest
from mock import Mock

from products.dependencies import Storage


@pytest.fixture
def storage(config):
    provider = Storage()
    provider.container = Mock(config=config)
    provider.setup()
    return provider.get_dependency({})


def test_get_fails_on_not_found(storage):
    with pytest.raises(storage.NotFound) as exc:
        storage.get(1)
    assert 'Product ID 1 does not exist' == exc.value.args[0]


def test_get_a_product(storage, products):
    product = storage.get('2')
    assert '2' == product['id']
    assert 'Yamaha' == product['title']
    assert 328 == product['maximum_speed']
    assert 5 == product['passenger_capacity']
    assert 10 == product['in_stock']


def test_get_multiple_products(storage, products):
    products = storage.getSpecificList('2,4')
    product_examples = [
        {
            "id": '2',
            "title": 'Yamaha',
            "maximum_speed": 328,
            "passenger_capacity": 5,
            "in_stock": 10
        },
        {
            "id": '4',
            "title": 'Toyota',
            "maximum_speed": 235,
            "passenger_capacity": 7,
            "in_stock": 15
        }
    ]

    assert (product_examples == sorted(list(products), key=lambda x: x['id']))


def test_list(storage, products):
    listed_products = storage.list()
    assert (
        products == sorted(list(listed_products), key=lambda x: x['id']))


def test_create(product, redis_client, storage):

    storage.create(product)

    stored_product = redis_client.hgetall('products:1')

    assert product['id'] == stored_product[b'id'].decode('utf-8')
    assert product['title'] == stored_product[b'title'].decode('utf-8')
    assert product['maximum_speed'] == int(stored_product[b'maximum_speed'])
    assert product['passenger_capacity'] == (
        int(stored_product[b'passenger_capacity']))
    assert product['in_stock'] == int(stored_product[b'in_stock'])


def test_create_list(products, redis_client, storage):

    storage.createList({'products': products})

    for product in products:
        stored_product = redis_client.hgetall('products:{}'.format(product['id']))
        assert product['id'] == stored_product[b'id'].decode('utf-8')
        assert product['title'] == stored_product[b'title'].decode('utf-8')
        assert product['maximum_speed'] == int(stored_product[b'maximum_speed'])
        assert product['passenger_capacity'] == (
            int(stored_product[b'passenger_capacity']))
        assert product['in_stock'] == int(stored_product[b'in_stock'])


def test_decrement_stock(storage, create_product, redis_client):
    create_product(id=5, title='Mercedez', in_stock=25)
    create_product(id=6, title='Ferreri', in_stock=26)
    create_product(id=7, title='Huyndai', in_stock=27)

    in_stock = storage.decrement_stock(5, 4)

    assert 21 == in_stock
    product_one, product_two, product_three = [
        redis_client.hgetall('products:{}'.format(id_))
        for id_ in (5, 6, 7)]
    assert b'21' == product_one[b'in_stock']
    assert b'26' == product_two[b'in_stock']
    assert b'27' == product_three[b'in_stock']
