import json

from mock import call
from gateway.exceptions import OrderNotFound, ProductNotFound


class TestGetProduct(object):
    def test_can_get_product_list(self, gateway_service, web_session):
        # gateway_service.products_rpc.getSpecificList.return_value = [
        #     {
        #         "maximum_speed": 300,
        #         "id": "2",
        #         "title": "Yamaha",
        #         "in_stock": 10,
        #         "passenger_capacity": 7
        #     },
        #     {
        #         "maximum_speed": 300,
        #         "id": "1",
        #         "title": "Honda",
        #         "in_stock": 10,
        #         "passenger_capacity": 7
        #     }
        # ]

        # response = web_session.get('/products/1,2')
        assert 1
        # assert response.status_code == 200
        # assert response.json()['data'] == [
        #     {
        #         "maximum_speed": 300,
        #         "id": "2",
        #         "title": "Yamaha",
        #         "in_stock": 10,
        #         "passenger_capacity": 7
        #     },
        #     {
        #         "maximum_speed": 300,
        #         "id": "1",
        #         "title": "Honda",
        #         "in_stock": 10,
        #         "passenger_capacity": 7
        #     }
        # ]

    # def test_can_get_product(self, gateway_service, web_session):
    #     gateway_service.products_rpc.get.return_value = {
    #         "in_stock": 10,
    #         "maximum_speed": 250,
    #         "id": "1",
    #         "passenger_capacity": 7,
    #         "title": "Honda"
    #     }
    #
    #     response = web_session.get('/product/1')
    #
    #     assert response.status_code == 200
    #     assert gateway_service.products_rpc.get.call_args_list == [
    #         call("1")
    #     ]
    #     assert response.json()['data'] == [{
    #         "in_stock": 10,
    #         "maximum_speed": 250,
    #         "id": "1",
    #         "passenger_capacity": 7,
    #         "title": "Honda"
    #     }]
    #
    # def test_product_not_found(self, gateway_service, web_session):
    #     gateway_service.products_rpc.get.side_effect = (
    #         ProductNotFound('Product ID {} does not exist'.format('foo'))
    #     )
    #
    #     # call the gateway service to get order #1
    #     response = web_session.get('/product/foo')
    #
    #     assert response.status_code == 200
    #     payload = response.json()
    #     assert payload['error'] == 'Missing'
    #     assert payload['message'] == 'Product ID {} does not exist'.format('foo')
    #
    # def test_can_get_all_products(self, gateway_service, web_session):
    #     gateway_service.products_rpc.list.return_value = [
    #         {
    #             "in_stock": 10,
    #             "maximum_speed": 250,
    #             "id": "1",
    #             "passenger_capacity": 7,
    #             "title": "Honda"
    #         },
    #         {
    #             "id": "2",
    #             "in_stock": 14,
    #             "title": "Yamaha",
    #             "passenger_capacity": 5,
    #             "maximum_speed": 300
    #         }
    #     ]
    #
    #     response = web_session.get('/products/*')
    #
    #     assert response.status_code == 200
    #     assert response.json()['data'] == [
    #         {
    #             "in_stock": 10,
    #             "maximum_speed": 250,
    #             "id": "1",
    #             "passenger_capacity": 7,
    #             "title": "Honda"
    #         },
    #         {
    #             "id": "2",
    #             "in_stock": 14,
    #             "title": "Yamaha",
    #             "passenger_capacity": 5,
    #             "maximum_speed": 300
    #         }
    #     ]

class TestCreateProduct(object):
    def test_can_create_product(self, gateway_service, web_session):
        response = web_session.post(
            '/product',
            json.dumps({
                "in_stock": 10,
                "maximum_speed": 230,
                "id": "1",
                "passenger_capacity": 4,
                "title": "Honda"
            })
        )
        assert response.status_code == 200
        assert response.json()['data'] == [{'id': '1'}]
        assert gateway_service.products_rpc.create.call_args_list == [call({
                    "in_stock": 10,
                    "maximum_speed": 230,
                    "id": "1",
                    "passenger_capacity": 4,
                    "title": "Honda"
                   })]

    def test_create_product_fails_with_invalid_json(
        self, gateway_service, web_session
    ):
        response = web_session.post(
            '/product', 'NOT-JSON'
        )
        assert response.status_code == 200
        assert response.json()['error'] == 'BAD_REQUEST'

    def test_create_product_fails_with_invalid_data(
        self, gateway_service, web_session
    ):
        response = web_session.post(
            '/product',
            json.dumps({"id": 1})
        )
        assert response.status_code == 200
        assert response.json()['error'] == 'INVALID_SCHEMA'

class TestGetOrder(object):

    def test_can_get_order(self, gateway_service, web_session):
        # setup mock orders-service response:
        gateway_service.orders_rpc.getOrder.return_value = {
            'id': 1,
            'products': [
                {
                    'id': '1',
                    'quantity': 2,
                    'product_id': 'Honda',
                    'price': 200.00,
                    'currency': 'USD'
                },
                {
                    'id': '2',
                    'quantity': 1,
                    'product_id': 'Yamaha',
                    'price': 400.00,
                    'currency': 'USD'
                }
            ]
        }

        # setup mock products-service response:
        gateway_service.products_rpc.list.return_value = [
            {
                'id': '1',
                'title': 'Honda',
                'maximum_speed': 250,
                'in_stock': 3,
                'passenger_capacity': 5
            },
            {
                'id': '2',
                'title': 'Yamaha',
                'maximum_speed': 200,
                'in_stock': 1,
                'passenger_capacity': 4
            },
        ]

        # call the gateway service to get order #1
        response = web_session.get('/order/1')
        assert response.status_code == 200

        expected_response = {
            'id': 1,
            'order_details': [
                {
                    'id': 1,
                    'quantity': 2,
                    'product_id': 'Honda',
                    # 'image':
                    #     'http://example.com/honda.jpg',
                    'product': {
                        'id': '1',
                        'title': 'Honda',
                        'maximum_speed': 250,
                        'in_stock': 3,
                        'passenger_capacity': 5
                    },
                    'price': '200.00'
                },
                {
                    'id': 2,
                    'quantity': 1,
                    'product_id': 'Yamaha',
                    # 'image':
                    #     'http://example.com/airship/images/the_enigma.jpg',
                    'product': {
                        'id': '2',
                        'title': 'Yamaha',
                        'maximum_speed': 200,
                        'in_stock': 1,
                        'passenger_capacity': 4
                    },
                    'price': '400.00'
                }
            ]
        }
        assert expected_response == response.json()

        # check dependencies called as expected
        assert [call(1)] == gateway_service.orders_rpc.getOrder.call_args_list
        assert [call()] == gateway_service.products_rpc.list.call_args_list
#
#     def test_order_not_found(self, gateway_service, web_session):
#         gateway_service.orders_rpc.getOrder.side_effect = (
#             OrderNotFound('missing'))
#
#         # call the gateway service to get order #1
#         response = web_session.get('/order/1')
#         assert response.status_code == 404
#         payload = response.json()
#         assert payload['error'] == 'ORDER_NOT_FOUND'
#         assert payload['message'] == 'missing'
#
#
