import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch

from constants import *

es = Elasticsearch()

top_judges = {
    "aggs": {
        "result": {
            "terms": {"field": "judges.name"}
        }
    }
}

monthly_histogram = {
    "aggs": {
        "result": {
            "date_histogram": {
                "field": "judgmentDate",
                "interval": "month",
                "format": "MM",
            }
        }
    }
}

judges_search = es.search(index=index_name, body=top_judges)
top_buckets = judges_search['aggregations']['result']['buckets'][:3]
for bucket in top_buckets:
    print(bucket)

monthly_search = es.search(index=index_name, body=monthly_histogram)
monthly_buckets = monthly_search['aggregations']['result']['buckets']
hist = dict((x['key_as_string'], x['doc_count']) for x in monthly_buckets)
plt.bar(list(hist.keys()), hist.values(), color='g')
plt.show()
