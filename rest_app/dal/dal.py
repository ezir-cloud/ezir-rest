import uuid
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
def bulk_json_data(api_repo_info,index):
    for doc in api_repo_info:

         if '['"index" not in doc:
            yield {
                "_index":index,
                "_id" : uuid.uuid4(),
                "_source":doc
            }


def insert_api_repo_info(index, api_repo_info):

    try:

        helpers.bulk(es, bulk_json_data(api_repo_info, index))

    except Exception as err:
        import traceback
        print("Elasticsearch index() ERRPR",traceback.format_exc())


def get_api_repo_info(index,repo_name):
    try:
        get_file_details = es.search(index=index, body={"query": {"match": {"name": repo_name}}})

    except Exception as err:
        import traceback
        print("Elasticsearch search() ERRPR", traceback.format_exc())

    return get_file_details
