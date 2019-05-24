from nameko.exceptions import registry, RemoteError



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

class NotFound(Exception):
    def __init__(self, message):
        words_list = message.split(' ')
        self.message = ' '.join(words_list[1:])


@remote_error('RemoteError')
class OutOfStock(Exception):
    def __init__(self, message):
        words_list = message.split(' ')
        self.message = ' '.join(words_list[1:])
        # super(OutOfStock, self).__init__(self.message)



