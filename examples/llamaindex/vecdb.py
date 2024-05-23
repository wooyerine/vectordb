from pymilvus import (
    Hit,
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import openai
import json
from logging_ import to_file

openai.api_key = ""
HOST = '127.0.0.1'
PORT = 19530
DIM = 1536

class VectorDB():
    def __init__(self):
        pass

    def connect(self, service):
        connections.connect(host=f'{HOST}', port=PORT)
        if service == 'leetcode':
            # if utility.has_collection(f'{service}'):
            #     utility.drop_collection(f'{service}')
            fields = [
              FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
              FieldSchema(name='pNumber', dtype=DataType.INT64),
              FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='example', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='constraint', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='output', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIM),
            ]
            schema = CollectionSchema(fields=fields)
            collection = Collection(name=f'{service}', schema=schema)
            collection.create_index(field_name="embedding", index_params={
                  "metric_type": "L2",
                  "index_type": "IVF_FLAT",
                  "params": {"nlist": 128},
              })
            collection.load()
            return collection
            # collection = Collection(name=f'{service}')
            # collection.load()
            # return collection
        if service == 'grepp':
            return collection
    
    def embed(self, texts):
        embeddings = openai.Embedding.create(
            input=texts,
            engine='text-embedding-3-small'
        )
        return [x['embedding'] for x in embeddings['data']]
    
    def ingest(self, collection, data):
        if collection.name == 'leetcode':
            data.append(self.embed(data[3]))
            collection.insert(data=data)

    def query(self, collection, query, top_k=5):
        response = collection.search(
            self.embed(query), 
            anns_field='embedding', 
            param={
                "metric_type": "L2",
                "params": {"ef": 64},
            },
            limit=top_k,
            output_fields= ['title', 'level',  'description', 'example', 'constraint', 'output'],
          )
        # print(response[0][0])
        # print(type(response[0][0]))
        def json_default(value):
            if isinstance(value, Hit):
                return str(value)
            raise TypeError('not JSON serializable')

        result = json.dumps(response, default=json_default, indent=4)
        to_file('./query/response.log', result)
        return result
        # return response

