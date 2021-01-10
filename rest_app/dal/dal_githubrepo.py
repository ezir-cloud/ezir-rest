import uuid
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()


def bulk_json_data(api_file_info,index):
    for doc in api_file_info:
         if '['"index" not in doc:
            yield {
                "_index":index,
                "_id" : uuid.uuid4(),
                "_source":doc
            }


def insert_api_repo_info(api_repo_info,index):
    try:
        repo_info_response = helpers.bulk(es,bulk_json_data(api_repo_info, index))
    except Exception as err:
        import traceback
        print("Elasticsearch bulk() ERRPR",traceback.format_exc())

def search_repo_by_name(index, repo_name):
    try:
        get_file_details =es.search(index=index, body={"query" :{"match": {"file_name" :repo_name } }})
    except Exception as err:
        import traceback
        print("Elasticsearch search() ERRPR",traceback.format_exc())
    return get_file_details