import pytest

from hashids import Hashids
from mock import call
from nameko.exceptions import RemoteError

from orders.models import Order, OrderDetail
from orders.schemas import OrderSchema, OrderDetailSchema

hashids = Hashids(min_length=10,
                      alphabet='0123456789abcdef',
                      salt='A secrect key')

@pytest.fixture
def order(db_session):
    order = Order()
    db_session.add(order)
    db_session.commit()

    return order

@pytest.fixture
def order_list(db_session):
    order_list = Order()
    db_session.add(order)
    db_session.commit()

    return order


@pytest.fixture
def order_details(db_session, order):
    db_session.add_all([
        OrderDetail(
            order=order, product_id="1", price=99.51, quantity=1,
            product_name="Honda", currency="usd"
        ),
        OrderDetail(
            order=order, product_id="2", price=30.99, quantity=8,
            product_name="Yamaha", currency="usd"
        )
    ])
    db_session.commit()
    return order_details


def test_get_order(orders_rpc, order):
    hash_id = hashids.encrypt(1)
    response = orders_rpc.getOrder(hash_id)
    assert response['id'] == order.id

# TODO
def test_get_order_list(orders_rpc, order_list):
    pass

@pytest.mark.usefixtures('db_session')
def test_will_raise_when_order_not_found(orders_rpc):
    with pytest.raises(RemoteError) as err:
        hash_id = hashids.encrypt(1)
        orders_rpc.getOrder(hash_id)
    assert err.value.value == 'Order with id {} not found'.format(hash_id)


@pytest.mark.usefixtures('db_session')
def test_can_create_order(orders_service, orders_rpc):
    order_details = [
        {
            'product_id': "1",
            'price': 99.99,
            'quantity': 1,
            'product_name': "Honda",
            'currency': "usd"
        },
        {
            'product_id': "2",
            'price': 5.99,
            'quantity': 8,
            'product_name': "Yamaha",
            'currency': "usd"
        }
    ]
    hash_id = hashids.encrypt(1)

    new_order = orders_rpc.createOrder(
        OrderDetailSchema(many=True).dump(order_details).data
    )

    assert new_order['id'] > 0
    assert len(new_order['order_details']) == len(order_details)
    assert [call(
        'order_created', {'order': {
            'id': 1,
            'hash_id': hash_id,
            'order_details': [
                {
                    'price': '99.99',
                    'product_id': "1",
                    'quantity': 1,
                    'product_name': "Honda",
                    'currency': "usd"
                },
                {
                    'price': '5.99',
                    'product_id': "2",
                    'quantity': 8,
                    'product_name': "Yamaha",
                    'currency': "usd"
                }
            ]}}
    )] == orders_service.event_dispatcher.call_args_list


@pytest.mark.usefixtures('db_session', 'order_details')
def test_can_update_order(orders_rpc, order):
    order_payload = OrderSchema().dump(order).data
    for order_detail in order_payload['order_details']:
        order_detail['quantity'] += 1

    updated_order = orders_rpc.updateOrder(order_payload)

    assert updated_order['order_details'] == order_payload['order_details']


def test_can_delete_order(orders_rpc, order, db_session):
    orders_rpc.deleteOrder(order.id)
    assert not db_session.query(Order).filter_by(id=order.id).count()
