# from nameko.events import event_handler
from nameko.rpc import rpc

from products import dependencies, schemas
from util.Logging import init_logger


class ProductsService(object):

    name = 'products'

    storage = dependencies.Storage()

    def __init__(self):
        self.logger = init_logger(name=self.name)

    @rpc
    def get(self, product_id):
        try:
            product = self.storage.get(product_id)
        except ValueError:
            raise
        except Exception as ex:
            self.logger.info(ex)
            raise

        return schemas.Product().dump(product).data

    @rpc
    def list(self):
        products = self.storage.list()
        return schemas.Product(many=True).dump(products).data

    @rpc
    def getSpecificList(self, product_ids_str):
        products_list = self.storage.getSpecificList(product_ids_str)
        return schemas.Product(many=True).dump(products_list).data

    @rpc
    def checkSpecificList(self, order_data):
        # Get product ids from the order into a list of String
        product_id_list = []
        for item in order_data['order_details']:
            product_id_list.append(item['product_id'])
        product_ids_str = ','.join(product_id_list)

        products_list = self.storage.getSpecificList(product_ids_str)
        return schemas.Product(many=True).dump(products_list).data

    @rpc
    def create(self, product):
        validated_product = schemas.Product(strict=True).load(product).data
        self.storage.create(validated_product)

    @rpc
    def createList(self, products):
        product_list = schemas.ProductList(strict=True).load(products).data
        self.storage.createList(product_list)

    @rpc
    def delete(self, product):

        try:
            validated_product = schemas.Product(strict=True).load(product).data
            self.storage.delete(validated_product)

        except Exception as ex:
            self.logger.info(ex)
            raise

    # @event_handler('orders', 'order_created')
    @rpc
    def handleOrderCreated(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])

    @rpc
    def handleOrderUpdated(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])

    @rpc
    def handleCartUpdated(self, payload):
        for product in payload['order']['order_details']:
            self.storage.check_stock(
                product['product_id'], product['quantity'])
