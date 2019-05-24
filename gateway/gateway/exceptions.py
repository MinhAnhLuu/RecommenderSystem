from nameko.exceptions import registry


def remote_error(exc_path):
    """
    Decorator that registers remote exception with matching ``exc_path``
    to be deserialized to decorated exception instance, rather than
    wrapped in ``RemoteError``.
    """

    def wrapper(exc_type):
        registry[exc_path] = exc_type
        return exc_type

    return wrapper


@remote_error('orders.exceptions.NotFound')
class OrderNotFound(Exception):
    """
    If the orders service raises a ``NotFound`` error from an RPC call,
    The ``RemoteError`` will be transformed and raised locally as this
    exception instead.
    """
    # pass

    def __init__(self, message):
        self.message = message


@remote_error('products.exceptions.NotFound')
class ProductNotFound(Exception):
    # pass
    def __init__(self, message):
        self.message = message

@remote_error('products.exceptions.ProductExisted')
class ProductExisted(Exception):
    # pass
    def __init__(self, message):
        self.message = message

@remote_error('orders.exceptions.OutOfStock')
@remote_error('products.exceptions.OutOfStock')
class ProductOutOfStock(Exception):
    # pass
    def __init__(self, message):
        self.message = message
