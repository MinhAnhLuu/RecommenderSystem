import json

from marshmallow import ValidationError
from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from werkzeug import Response
from hashids import Hashids

from gateway.entrypoints import http
from gateway.exceptions import OrderNotFound, ProductNotFound, ProductOutOfStock, ProductExisted
from gateway.schemas import CreateOrderSchema, \
                            GetOrderSchema, \
                            ProductSchema, \
                            CreateProductSchemaList
from util.ResponseFormat import RequestHandler
from util.Logging import init_logger
from util.ReadConfig import ReadConfig
from util.MemCache import Memoize

import logging

# TODO

# 1. Add header ‘Access-Control-Allow-Origin’: "*" to response
# 2. Add more catch Exception for recommender service

class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    orders_rpc = RpcProxy('orders')
    products_rpc = RpcProxy('products')
    recommender_rpc = RpcProxy('recommender')

    hashids = Hashids(min_length=10,
                      alphabet='0123456789abcdef',
                      salt='A secret key')

    def __init__(self):

        self.config = ReadConfig(config_file="gateway.ini",
                                 path_file="/home/docker/gateway/config")
        log_file = self.config.readConfig(section="location",
                                          key="folder") + self.name + ".out"

        self.logger = init_logger(name=self.name, log_file=log_file)
        self.logger.info("INIT %s..." % self.name)

    def __delete__(self, instance):
        pass

    @http(
        "GET", "/product/<string:product_id>",
        expected_exceptions=ProductNotFound
    )
    @Memoize(timeout=3600)
    def getProduct(self, request, product_id):
        """Gets product by `product_id`
        """
        try:
            product = self.products_rpc.get(product_id)

        except ProductNotFound as ex:

            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=product)),
            mimetype='application/json'
        )

    @http(
        "GET", "/products/<string:product_ids>",
        expected_exceptions=ProductNotFound
    )
    @Memoize(timeout=10)
    def getSpecificProducts(self, request, product_ids):
        """Gets products by `product_id` list
        """
        try:
            if '*' in product_ids:
                products = self.products_rpc.list()
            else:
                products = self.products_rpc.getSpecificList(product_ids)

        except ProductNotFound as ex:
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=products)),
            mimetype='application/json'
        )

    @http(
        "POST", "/product/add",
        expected_exceptions=(ValidationError, BadRequest)
    )
    def createProduct(self, request):
        """Create a new product - product data is posted as json

        Example request ::

            {
                "id": "1",
                "title": "Yamaha",
                "passenger_capacity": 7,
                "maximum_speed": 300,
                "in_stock": 10,
                "category": "Car"
            }


        The response contains the new product ID in a json document ::

            {"id": "1"}

        """
        schema = ProductSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            product_data = schema.loads(request.get_data(as_text=True)).data
            # Create the product
            self.products_rpc.create(product_data)
        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        except ProductExisted as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='ProductExisted',
                                                         message=str(ex))),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)

            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data={'id': product_data['id']})),
            mimetype='application/json'
        )

    @http(
        "POST", "/products/add",
        expected_exceptions=(ValidationError, BadRequest)
    )
    def createProductList(self, request):
        """Create a list of new products - product data is posted as json

        Example request ::
        {
            "products": [
                {
                    "id": "1",
                    "title": "Yamaha",
                    "passenger_capacity": 7,
                    "maximum_speed": 300,
                    "in_stock": 10
                },
                {
                    "id": "1",
                    "title": "Honda",
                    "passenger_capacity": 5,
                    "maximum_speed": 270,
                    "in_stock": 19
                }
            ]
        }

        The response contains the new product ID in a json document ::

            [{"id": "1"}, {"id": "2"}]

        """

        schema = CreateProductSchemaList(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.

            product_data = schema.loads(request.get_data(as_text=True)).data
            product_id_list = [{'id': product['id']} for product in product_data['products']]

            # Create products
            self.products_rpc.createList(product_data)

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        except ProductExisted as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='ProductExisted',
                                                         message=str(ex))),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=product_id_list)),
            mimetype='application/json'
        )

    @http(
        "POST", "/product/delete",
        expected_exceptions=(ValidationError, BadRequest)
    )
    def deleteProduct(self, request):
        """Create a new product - product data is posted as json

        Example request ::

            {
                "id": "1",
                "title": "Yamaha",
                "passenger_capacity": 7,
                "maximum_speed": 300,
                "in_stock": 10,
                "category": "Car"
            }


        The response contains the new product ID in a json document ::

            {message}

        """
        schema = ProductSchema(strict=True)

        try:
            product_data = schema.loads(request.get_data(as_text=True)).data

            # Delete the product
            self.products_rpc.delete(product_data)

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)

            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     message='Delete successful')),
            mimetype='application/json'
        )

    @http("GET", "/order/<string:hashed_order_id>",
          expected_exceptions=OrderNotFound)
    @Memoize(timeout=3600)
    def getOrder(self, request, hashed_order_id):
        """Gets the order details for the order given by `order_id`.

        Enhances the order details with full product details from the
        products-service.
        """
        try:
            order = self._getOrder(hashed_order_id)

        except OrderNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')
        # TODO
        # except InvalidRequestError as ex:
        # return

        except Exception as ex:
            self.logger.info(ex)

            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=order)),
            mimetype='application/json'
        )

    @http("GET", "/cart/show/",
          expected_exceptions=OrderNotFound)
    def showCart(self, request):
        """Gets the order details for the orders given by `hashed_order_ids`.

        Enhances the order details with full product details from the
        products-service.
        """
        try:
            customer_id = request.args['customer_id']
            orders = self.orders_rpc.showCart(customer_id)

        except OrderNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='Exception',
                                                         message=str(ex))),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=orders)),
            mimetype='application/json'
        )

    def _getOrder(self, hashed_order_id):
        # Retrieve order data from the orders service.
        # Note - this may raise a remote exception that has been mapped to
        # raise``OrderNotFound``

        try:
            order = self.orders_rpc.getOrder(hashed_order_id)
        except OrderNotFound as ex:
            self.logger.info(ex)
            raise OrderNotFound('Order with id {} not found'.format(hashed_order_id))

        # Retrieve all products from the products service
        product_map = {prod['id']: prod for prod in self.products_rpc.list()}

        # self.logger.info("product_map: %s" % product_map)
        # get the configured image root
        image_root = self.config.readConfig(section='location',
                                            key='PRODUCT_IMAGE_ROOT')

        # Enhance order details with product and image details.
        for item in order['order_details']:
            product_id = item['product_id']

            item['product'] = product_map[product_id]
            # Construct an image url.
            item['image'] = '{}/{}.jpg'.format(image_root, product_id)

        return order

    @http(
        "POST", "/order",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def createOrder(self, request):
        """Create a new order - order data is posted as json

        Example request ::

            {
                "order_details": [
                    {
                        "product_id": "1",
                        "product_name": "Honda",
                        "price": "99800",
                        "quantity": 1,
                        "currency": "usd"
                    },
                    {
                        "product_id": "2",
                        "price": "10000",
                        "product_name": "Yamaha",
                        "quantity": 2,
                        "id": "2",
                        "currency": "usd"
                    }
                ]
            }


        The response contains the new order ID in a json document ::

            {"data": '1234'}

        """

        schema = CreateOrderSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            order_data = schema.loads(request.get_data(as_text=True)).data

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        # Create the order
        # Note - this may raise `ProductNotFound`
        try:
            id_ = self._createOrder(order_data)

            # self.logger.info("id of Orders: %s" % id_)

        except ProductNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except ProductOutOfStock as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Insufficient',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         message=str(ex),
                                                         error='Exception')),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=id_)),
            mimetype='application/json')

    def _createOrder(self, order_data):
        product_id_list = []
        # Get product ids from the order
        for item in order_data['order_details']:
            product_id_list.append(item['product_id'])

        product_ids_str = ','.join(product_id_list)
        # Get available products as most as possible
        # Throw NotFound Exception when an product id is not found
        self.products_rpc.getSpecificList(product_ids_str)

        serialized_data = CreateOrderSchema().dump(order_data).data
        # Throw OutOfStock if a product is insufficient in quantity

        try:
            result = self.orders_rpc.createOrder(
                                    serialized_data['order_details']
                                    )

        except ProductOutOfStock as ex:
            self.logger.info("gateway._createOrder: %s" % ex)
            raise

        return result['hash_id']

    @http(
        "POST", "/order/<string:order_id>",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def updateOrder(self, request, order_id):
        """Update an available order - order data is posted as json

        Example request ::

            {
                "order_details": [
                    {
                        "product_id": "1",
                        "product_name": "Honda",
                        "price": "99800",
                        "quantity": 1,
                        "currency": "usd"
                    },
                    {
                        "price": "10000",
                        "product_name": "Yamaha",
                        "quantity": 2,
                        "product_id": "2",
                        "currency": "usd"
                    },
                ]
            }


        The response contains the new order ID in a json document ::

            {"id": '1234'}

        """

        schema = CreateOrderSchema(strict=True)

        try:
            # load input data through a schema (for validation)
            # Note - this may raise `ValueError` for invalid json,
            # or `ValidationError` if data is invalid.
            order_data = schema.loads(request.get_data(as_text=True)).data

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        # Create the order
        # Note - this may raise `ProductNotFound`
        try:
            serialized_data = CreateOrderSchema().dump(order_data).data

            # Throw OutOfStock if a product is insufficient in quantity

            _id = self.orders_rpc.updateOrder(
                serialized_data['order_details']
            )

        except ProductNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except ProductOutOfStock as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Insufficient',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         message=str(ex),
                                                         error='Exception')),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=_id)),
            mimetype='application/json')

    @http(
        "GET", "/recommend/user/",
        expected_exceptions=(ProductNotFound)
    )
    def get_recommend_by_ratings(self, request):
        """Test get Product from Service Product to Product Recommender"""

        try:
            header = dict()
            header["Access-Control-Allow-Origin"] = "*"
            title = request.args['title']
            k = int(request.args['k'])
            result = self.recommender_rpc.get_recommendations_by_ratings(title, k)
        except ProductNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json',
                headers=header
            )

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=result)),
            mimetype='application/json',
            headers=header
        )

    @http(
        "GET", "/recommend/content/",
        expected_exceptions=(ProductNotFound)
    )
    def get_recommend_by_overview(self, request):
        """Test get Product from Service Product to Product Recommender"""

        try:
            header = dict()
            header["Access-Control-Allow-Origin"] = "*"
            title = request.args['title']
            mode = request.args['mode']
            k = int(request.args['k'])
            result = self.recommender_rpc.get_recommendations_by_item(title, mode, k)

        except ProductNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json',
                headers=header
            )

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=result)),
            mimetype='application/json',
            headers=header
        )

    @http(
        "POST", "/cart/add/",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def processCart(self, request):

        try:
            # Validate Schema
            customer_id = request.args['customer_id']
            order_data = self._validateOrderSchema(request)

            # Update order and product
            result_message = self._processCart(order_data, customer_id)

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            message = "Invalid json: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='BAD_REQUEST',
                                                         message=message)),
                mimetype='application/json')

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            message = "Invalid schema: {}".format(exc)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         error='INVALID_SCHEMA',
                                                         message=message)),
                mimetype='application/json')

        except ProductNotFound as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Missing',
                                                         message=ex.message)),
                mimetype='application/json')

        except ProductOutOfStock as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=404,
                                                         error='Insufficient',
                                                         message=ex.message)),
                mimetype='application/json')

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         message=str(ex),
                                                         error='Exception')),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     message=result_message)),
            mimetype='application/json')

    def _processCart(self, order_data, customer_id):

        try:
            # Convert from Schema into JSON
            serialized_data = CreateOrderSchema().dump(order_data).data

            # Get available products to check whether product is available
            self.products_rpc.checkSpecificList(serialized_data)

            # result = self.orders_rpc.createOrder(serialized_data['order_details'])
            result_message = self.orders_rpc.processCart(serialized_data, customer_id)

        except ProductNotFound as ex:
            self.logger.info(ex)
            raise ProductNotFound("Product not found!")

        except ProductOutOfStock as ex:
            self.logger.info(ex)
            raise ProductOutOfStock("Product is out of stock!")

        except Exception as ex:
            self.logger.info(ex)
            raise

        return result_message

    def _validateOrderSchema(self, request):
        schema = CreateOrderSchema(strict=True)

        try:
            order_data = schema.loads(request.get_data(as_text=True)).data

        except ValueError as exc:
            self.logger.info("Invalid json: {}".format(exc))
            raise

        except ValidationError as exc:
            self.logger.info("Invalid schema: {}".format(exc))
            raise

        return order_data

    @http(
        "POST", "/cart/delete/",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def deleteCart(self, request):

        try:
            customer_id = request.args['customer_id']
            result_message = self._deleteCart(customer_id)

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         message=str(ex),
                                                         error='Exception')),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     message=result_message)),
            mimetype='application/json')

    def _deleteCart(self, customer_id):

        try:
            result_message = self.orders_rpc.deleteCart(customer_id)

        except Exception as ex:
            self.logger.info(ex)
            raise

        return result_message

    @http(
        "POST", "/cart/checkout/",
        expected_exceptions=(ValidationError, ProductNotFound, BadRequest)
    )
    def checkoutCart(self, request):

        try:
            customer_id = request.args['customer_id']
            result_message = self._checkoutCart(customer_id)

        except Exception as ex:
            self.logger.info(ex)
            return Response(
                json.dumps(RequestHandler.formatResponse(status_code=403,
                                                         message=str(ex),
                                                         error='Exception')),
                mimetype='application/json')

        return Response(
            json.dumps(RequestHandler.formatResponse(status_code=200,
                                                     data=result_message)),
            mimetype='application/json')

    def _checkoutCart(self, customer_id):

        try:
            result_message = self.orders_rpc.checkoutCart(customer_id)

        except Exception as ex:
            self.logger.info(ex)
            raise

        return result_message
