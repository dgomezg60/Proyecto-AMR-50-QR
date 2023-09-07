
from elasticsearch import Elasticsearch


class ElasticConection:
    __instance = None
    ##------------------------------------------------------------------- Singleton ----------------------------------------------------------------------------------------------
    ##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ElasticConection,cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        self.User = Elasticsearch(
        "https://localhost:9200",
        ca_certs="C://Users//dgomezg//Documents//elasticstack//elasticsearch-8.9.1-windows-x86_64//elasticsearch-8.9.1//config//certs//http_ca.crt",
        basic_auth=("david", "123456")
        )
        print(self.User.ping())