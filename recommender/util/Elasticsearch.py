import os
from elasticsearch import Elasticsearch


class ElasticSearch(object):
    host_name = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    port_name = os.getenv("ELASTICSEARCH_PORT", "9200")
    host = 'http://' + host_name + ':' + port_name

    def __init__(self):
        self.es = Elasticsearch([self.host])

    def check_health(self):
        return self.es.cluster.health()
