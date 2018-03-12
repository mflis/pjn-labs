from elasticsearch import Elasticsearch

from constants import *

es = Elasticsearch()

szkoda_query = {
    "query": {
        "match": {
            "textContent": "szkoda"
        }
    }
}
# exact match in all flex forms
uszczerbek_query = {
    "query": {
        "match_phrase": {
            "textContent": {
                "query": "trwały uszczerbek na zdrowiu",
            }
        }
    }
}

# does not preserve order of words
uszczerbek_slop_query = {
    "query": {
        "match_phrase": {
            "textContent": {
                "query": "trwały uszczerbek na zdrowiu",
                'slop': 2
            }
        }
    }
}


def print_results(query, print_all=False):
    print(f"query: {query}")
    response = es.search(index=index_name, body=query, size=100)
    if print_all:
        for text in response['hits']['hits']:
            print(text['_source']['textContent'])

    print("judgements matching query: %d " % response['hits']['total'])


print_results(szkoda_query)
print_results(uszczerbek_query)
print_results(uszczerbek_slop_query)
