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
        print("Elasticsearch bulk() ERRPR",traceback.format_exc())

def search_file_by_name(index,file_name):
    try:
        get_file_details =es.search(index=index, body={"query" :{"match": {"file_name" :file_name } }})
    except Exception as err:
        import traceback
        print("Elasticsearch search() ERRPR",traceback.format_exc())
    return get_file_details