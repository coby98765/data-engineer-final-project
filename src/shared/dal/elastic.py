from elasticsearch import Elasticsearch
from ..config import get_settings

from elasticsearch import Elasticsearch, helpers
from src.utils.logger import Logger
import os

# logger setup
logger = Logger.get_logger(index="persister_log",name="persister.elasticDAL.py")

class ElasticDAL:
    def __init__(self,index_name="podcasts"):
        HOST = os.getenv("ES_HOST", "http://localhost:9200")
        self.index_name = index_name
        self.request_timeout = 20
        self.verify_certs = True
        try:
            self.es = Elasticsearch(
                hosts=HOST,
                request_timeout=self.request_timeout,
                verify_certs=self.verify_certs
            )
            logger.info(f'ElasticDAL.init, connected to ElasticSearch.')
        except Exception as e:
            logger.error(f"ElasticDAL.init, Error: {e}")

    def map_index(self,report_map:dict):
        mapping = dict()
        mapping["mappings"] = dict()
        try:
            mapping["mappings"]["properties"] = report_map
            self.es.indices.create(
                index=self.index_name,
                body=mapping,
                ignore=400
            )
            logger.info(f'ElasticDAL.map_index, Index "{self.index_name}" created successfully with mapping.')
        except Exception as e:
            logger.error(f"ElasticDAL.map_index, Error: {e}")

    def insert_data(self,report):
        try:
            _id = report.pop("_id")
            self.es.index(
                index=self.index_name,
                id=_id,
                body=report
            )
            logger.info(f'ElasticDAL.insert_data, Indexed {_id} report.')

        except Exception as e:
            logger.error(f"ElasticDAL.insert_data, Error: {e}")

    def get_all(self):
        try:
            query_body = {
                "query": {
                    "match_all": {}
                }
            }
            response = self.es.search(
                index=self.index_name,
                body=query_body)
            logger.info(f'ElasticDAL.get_all, got all.')
            clean_res = self.res_cleaner(response["hits"]["hits"])
            return clean_res
        except Exception as e:
            logger.error(f"ElasticDAL.get_all, Error: {e}")
