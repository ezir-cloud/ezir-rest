import json
import uuid

import ndjson
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk


es = Elasticsearch()

def bulk_json_data(api_repo_info,index):
    for doc in api_repo_info:

         if '['"index" not in doc:
            yield {
                "_index":index,
                "_id" : uuid.uuid4(),
                "_source":doc
            }


def insert_api_repo_info(api_repo_info,index):

    print(index)
    print(api_repo_info)
    try:

        file_info_response = helpers.bulk(es, bulk_json_data(api_repo_info,index))
        print(file_info_response)

    except Exception as err:
        import traceback
        print("Elasticsearch index() ERRPR",traceback.format_exc())