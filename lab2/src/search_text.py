import matplotlib.pyplot as plt
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

top_judges = {
    "aggs": {
        "judges": {
            "terms": {"field": "judges.name"}
        }
    }
}

monthly_histogram = {
    "aggs": {
        "monthly": {
            "date_histogram": {
                "field": "judgmentDate",
                "interval": "month",
                "format": "MM",
            }
        }
    }
}


def print_results(query):
    print(f"query: {query}")
    res = es.search(index=index_name, body=query, size=100)
    for text in res['hits']['hits']:
        print(text['_source']['textContent'])
    print("judgements matching query: %d " % res['hits']['total'])


# print_results(szkoda_query)
# print_results(uszczerbek_query)
# print_results(uszczerbek_slop_query)
# print_results(top3_judges)

# res = es.search(index=index_name, body=top3_judges)
# top_buckets = res['aggregations']['judges']['buckets'][:3]
# for bucket in top_buckets:
#     print(bucket)

res = es.search(index=index_name, body=monthly_histogram)
histogram = res['aggregations']['monthly']['buckets']
hist = dict((x['key_as_string'], x['doc_count']) for x in histogram)
plt.bar(list(hist.keys()), hist.values(), color='g')
plt.show()
res = es.search(index=index_name, body=top_judges)
# top_buckets = res['aggregations']['judges']['buckets'][:3]
# for bucket in top_buckets:
#     print(bucket)
