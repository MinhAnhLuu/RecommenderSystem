from orders.models import Order, OrderDetail


def test_can_create_order(db_session):
    order = Order()
    db_session.add(order)
    db_session.commit()
    assert order.id > 0


def test_can_create_order_detail(db_session):
    order = Order()
    order_detail_1 = OrderDetail(
        order=order,
        product_id="1",
        product_name="Honda",
        price=100.50,
        quantity=10,
        currency="usd"
    )
    order_detail_2 = OrderDetail(
        order=order,
        product_id="2",
        product_name="Yamaha",
        price=99.50,
        quantity=20,
        currency="usd"

    )

    db_session.add_all([order_detail_1, order_detail_2])
    db_session.commit()

    assert order.id > 0
    for order_detail in order.order_details:
        assert order_detail.id > 0
    assert order_detail_1.product_id == "1"
    assert order_detail_1.price == 100.50
    assert order_detail_1.quantity == 10
    assert order_detail_1.currency == "usd"
    assert order_detail_1.product_name == "Honda"
    assert order_detail_2.product_id == "2"
    assert order_detail_2.price == 99.50
    assert order_detail_2.quantity == 20
    assert order_detail_2.currency == "usd"
    assert order_detail_2.product_name == "Yamaha"
