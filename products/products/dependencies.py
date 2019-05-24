from nameko.extensions import DependencyProvider
import redis

from products.exceptions import NotFound, OutOfStock, ProductExisted
from util.Logging import init_logger
import logging

REDIS_URI_KEY = 'REDIS_URI'


class StorageWrapper:
    """
    Product storage

    A very simple example of a custom Nameko dependency. Simplified
    implementation of products database based on Redis key value store.
    Handling the product ID increments or keeping sorted sets of product
    names for ordering the products is out of the scope of this example.

    """

    NotFound = NotFound
    name = 'redis_storage'

    def __init__(self, client):
        self.client = client
        self.logger = init_logger(name=self.name)
        self.logger.info("INIT %s..." % self.name)

    def _format_key(self, product_id):
        return 'products:{}'.format(product_id)

    def _from_hash(self, document):
        return {
            'id': document[b'id'].decode('utf-8'),
            'title': document[b'title'].decode('utf-8'),
            'passenger_capacity': int(document[b'passenger_capacity']),
            'maximum_speed': int(document[b'maximum_speed']),
            'in_stock': int(document[b'in_stock'])
        }

    def _generate_id_from_key(self, keys):
        # Split x from products:x
        return [key.decode().split(':')[-1] for key in keys]

    def get(self, product_id):
        product = self.client.hgetall(self._format_key(product_id))
        if not product:
            raise NotFound('Product ID {} does not exist'.format(product_id))
        else:
            return self._from_hash(product)

    def list(self):
        keys = self.client.keys(self._format_key(product_id='*'))
        for key in keys:
            yield self._from_hash(self.client.hgetall(key))

    def getSpecificList(self, specific_product_ids):

        product_ids_str = '[' + specific_product_ids.replace(',', '|') + ']'
        specific_product_list = specific_product_ids.split(',')

        keys = self.client.keys(self._format_key(product_ids_str))

        if not keys:
            raise NotFound('Product IDs {} does not exist'.format(specific_product_ids))
        elif len(specific_product_list) != len(keys):
            unavailable_product_id_set = frozenset(specific_product_list) - \
                                         frozenset(self._generate_id_from_key(keys=keys))

            raise NotFound('Product ID {} does not exist'.format(unavailable_product_id_set))
        else:
            for key in keys:
                yield self._from_hash(self.client.hgetall(key))

    def isExisted(self, product_id):
        product = self.client.hgetall(self._format_key(product_id))
        if product:
            return True
        else:
            return False

    def create(self, product):
        existed_product = self.isExisted(product['id'])
        if not existed_product:
            self.client.hmset(self._format_key(product['id']), product)
        else:
            raise ProductExisted('Product ID {} existed in database'.format(product['id']))

    def createList(self, product_list):
        for product in product_list['products']:
            existed_product = self.isExisted(product['id'])
            if existed_product:
                raise ProductExisted('Product ID {} existed in database'.format(product['id']))

        for product in product_list['products']:
            self.client.hmset(self._format_key(product['id']), product)

    def delete(self, product):
        self.client.delete(self._format_key(product['id']))

    def decrement_stock(self, product_id, amount):
        in_stock_amount = self.client.hget(self._format_key(product_id=product_id),
                                           'in_stock')

        if int(in_stock_amount) >= int(amount):
            return self.client.hincrby(
                self._format_key(product_id), 'in_stock', -amount)
        else:
            raise OutOfStock('Product ID {} is insufficient'.format(product_id))

    def increment_stock(self, product_id, amount):
        return self.client.hincrby(
            self._format_key(product_id), 'in_stock', amount)

    def check_stock(self, product_id, amount):
        in_stock_amount = self.client.hget(self._format_key(product_id=product_id), 'in_stock')

        if int(in_stock_amount) < int(amount):
            raise OutOfStock('Product ID {} is insufficient'.format(product_id))


class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url(
            self.container.config.get(REDIS_URI_KEY))

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)
