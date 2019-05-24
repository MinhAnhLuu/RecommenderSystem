class NotFound(Exception):
    def __init__(self, message):
        words_list = message.split(' ')
        self.message = ' '.join(words_list[1:])

class ProductExisted(Exception):
    def __init__(self, message):
        words_list = message.split(' ')
        self.message = ' '.join(words_list[1:])

class OutOfStock(Exception):
    pass