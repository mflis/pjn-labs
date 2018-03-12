from elasticsearch import Elasticsearch

create_index_body = {
    'settings': {
        # just one shard, no replicas for testing
        'number_of_shards': 1,
        'number_of_replicas': 0,

        'analysis': {
            'analyzer': {
                'polish': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ["morfologik_stem"],
                }
            }
        }
    },
    'mappings': {
        'judgement': {
            'properties': {
                'textContent': {'type': 'text', 'analyzer': 'polish'},
                'judgmentDate': {'type': 'date'},
                'courtCases.caseNumber': {'type': 'keyword'},
                'judges.name': {'type': 'text', 'analyzer': 'polish'},  ## maybe standard analyzer?
            }
        }
    }
}

es = Elasticsearch()
es.indices.delete(index='myindex', ignore=[400, 404])
es.indices.create(index='myindex', body=create_index_body)
