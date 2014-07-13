from elasticsearch import Elasticsearch
from datetime import datetime


doc = {
    'author': 'Felix',
    'text': 'Alo!',
    'timestamp': datetime.now()
}

INDEX = 'test-people'
DOC_TYPE = 'test-person'
INDEX_ID = 1

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# ignore 400 cause by IndexAlreadyExistsException when creating an index
index_res = es.indices.create(index=INDEX, ignore=[400])

