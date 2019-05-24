from nameko.rpc import RpcProxy, rpc
from util.Logging import init_logger
from util.Elasticsearch import ElasticSearch
from util.RecommenderItemBased import  RecommenderItemBased

class RecommenderService(object):
    name = 'recommender'
    product_rpc = RpcProxy('products')

    def __init__(self):
        self.logger = init_logger(name=self.name)
        self.es = ElasticSearch()
        self.recommender = RecommenderItemBased()

    @rpc
    def test(self):
        res = self.es.check_health()
        return res

    @rpc
    def get_recommendations_by_ratings(self, title, k):
        res = self.recommender.get_recommendations_by_ratings(title, k)
        return res

    @rpc
    def get_recommendations_by_item(self, title, mode, k):
        res = self.recommender.get_recommendations_by_items(title, mode, k)
        return res
