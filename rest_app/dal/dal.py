import json
import uuid
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk

es = Elasticsearch()


def bulk_json_data(api_file_info,index):
    for doc in api_file_info:
         if '['"index" not in doc:
            yield {
                "_index":index,
                "_id" : uuid.uuid4(),
                "_source":doc
            }


def insert_api_file_info(api_file_info,index):
    try:
        file_info_response = helpers.bulk(es,bulk_json_data(api_file_info,index))
    except Exception as err:
        import traceback
        print("Elasticsearch index() ERRPR",traceback.format_exc())
