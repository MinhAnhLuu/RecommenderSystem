from hashids import Hashids

from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from nameko.rpc import RpcProxy
from nameko.exceptions import RemoteError

from orders.exceptions import NotFound, OutOfStock
from orders.models import DeclarativeBase, Order, OrderDetail, DeclarativeOrderDetail
from orders.schemas import OrderSchema, OrderDetailSchema

from util.Logging import init_logger
import logging

class OrdersService(object):

    name = 'orders'
    products_rpc = RpcProxy('products')

    event_dispatcher = EventDispatcher()
    order_db = DatabaseSession(DeclarativeBase)
    order_detail_db = DatabaseSession(DeclarativeOrderDetail)

    hashids = Hashids(min_length=10,
                      alphabet='0123456789abcdef',
                      salt='A secret key')

    def __init__(self):
        self.logger = init_logger(name=self.name)

    @rpc
    def getOrder(self, hashed_order_id):
        order_id = self.hashids.decrypt(hashid=hashed_order_id)
        # self.logger.info("order_id: %s" % order_id)
        order = self.order_db.query(Order).get(order_id)

        if not order:
            raise NotFound('Order with id {} not found'.format(hashed_order_id))

        # Hide real Id from DB
        data = OrderSchema().dump(order).data
        data['id'] = hashed_order_id

        return data

    @rpc
    def createOrder(self, order_details):

        order = Order(
            order_details=[
                OrderDetail(
                    product_id=order_detail['product_id'],
                    product_name=order_detail['product_name'],
                    price=order_detail['price'],
                    quantity=order_detail['quantity'],
                    currency=order_detail['currency']
                )
                for order_detail in order_details
            ]
        )

        self.order_db.add(order)
        self.order_db.commit()

        order = OrderSchema().dump(order).data

        try:
            # self.event_dispatcher('order_created', {
            #         'order': order
            #     })
            self.products_rpc.handleOrderCreated({'order': order})
        except RemoteError as ex:
            self.logger.info("orders.createOrder: %s" % ex)
            raise OutOfStock(str(ex))

        # self.logger.info("createOrder: order: %s" % order)
        # Hide real Id from DB
        order['hash_id'] = self.hashids.encrypt(order['id'])

        return order

    @rpc
    def deleteOrder(self, order_id):
        order = self.order_db.query(Order).get(order_id)
        self.order_db.delete(order)
        self.order_db.commit()

    @rpc
    def showCart(self, customer_id):

        try:
            # Search order by customer ID and status, to get order id
            order = self.order_db.query(Order).filter_by(customer_id=customer_id, status='CREATED').first()
            order_id = order.id
            product_list = self.order_detail_db.query(OrderDetail).filter_by(order_id=order_id).all()

            data_list = []
            for product in product_list:
                data = OrderDetailSchema().dump(product).data
                data['id'] = self.hashids.encrypt(product.id)
                data_list.append(data)

        except Exception as ex:
            self.logger.info("orders.updateOrder: %s" % ex)
            raise NotFound('Order with customer id {} not found'.format(customer_id))

        return data_list

    @rpc
    def processCart(self, order, customer_id):

        existed_order = self.order_db.query(Order).filter_by(status='CREATED', customer_id=customer_id).first()

        try:
            self.products_rpc.handleCartUpdated({'order': order})
            if existed_order:
                return self._updateQuantityCart(order, existed_order)
            else:
                return self._createCart(order, customer_id)

        except RemoteError as ex:
            self.logger.info("orders.updateOrder: %s" % ex)
            raise OutOfStock(str(ex))

        except Exception as ex:
            self.logger.info("orders.updateOrder: %s" % ex)
            raise OutOfStock(str(ex))

    def _updateQuantityCart(self, order, existed_order):
        temp_dict_1 = {}
        temp_dict_2 = {}

        for update_product in order['order_details']:
            temp_dict_1[update_product['product_id']] = update_product

        for existed_product in existed_order.order_details:
            temp_dict_2[existed_product.product_id] = {
                'product_id': existed_product.product_id,
                'order_id': existed_order.id,
                'product_name': existed_product.product_name,
                'price': existed_product.price,
                'quantity': existed_product.quantity
            }

        temp_dict_2.update(temp_dict_1)

        self.order_detail_db.query(OrderDetail).filter_by(order_id=existed_order.id).delete()
        self.order_detail_db.add_all([OrderDetail(
                    product_id=update_product['product_id'],
                    order_id=existed_order.id,
                    product_name=update_product['product_name'],
                    price=update_product['price'],
                    quantity=update_product['quantity'],
                    currency=update_product['currency']
                ) for update_product in temp_dict_2.values()])


        # Update quantity
        self.order_db.commit()

        # Quantity = 0
        self.order_detail_db.query(OrderDetail).filter_by(quantity=0).delete()
        self.order_detail_db.commit()
        return "Update successful!"

    def _createCart(self, order_data, customer_id):

        order = Order(
            customer_id=customer_id,
            order_details=[
                OrderDetail(
                    product_id=order_detail['product_id'],
                    product_name=order_detail['product_name'],
                    price=order_detail['price'],
                    quantity=order_detail['quantity'],
                    currency=order_detail['currency'],
                )
                for order_detail in order_data["order_details"]
            ]
        )

        self.order_db.add(order)
        self.order_db.commit()

        order = OrderSchema().dump(order).data

        # Hide real Id from DB
        order['hash_id'] = self.hashids.encrypt(order['id'])

        return "Create successful!"

    @rpc
    def deleteCart(self, customer_id):

        try:
            # Search order by customer ID and status
            order = self.order_db.query(Order).filter_by(customer_id=customer_id, status='CREATED').first()
            order_id = order.id

            logging.warning(">> ", order_id)
            # Delete order details
            self.order_detail_db.query(OrderDetail).filter_by(order_id=order_id).delete()
            self.order_detail_db.commit()

            # Delete order
            self.order_db.query(Order).filter_by(customer_id=customer_id, status='CREATED').delete()
            self.order_db.commit()

        except Exception as ex:
            self.logger.info("orders.updateOrder: %s" % ex)
            raise OutOfStock(str(ex))

        return "Delete Successful"

    @rpc
    def checkoutCart(self, customer_id):

        try:
            order = self.order_db.query(Order).filter_by(customer_id=customer_id, status='CREATED').first()
            order.status = "DONE"
            self.order_db.commit()

        except Exception as ex:
            self.logger.info("orders.updateOrder: %s" % ex)
            raise OutOfStock(str(ex))

        return "Checkout Successful"
