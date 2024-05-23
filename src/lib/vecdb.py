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
from config import Milvus, Openai

openai.api_key = Openai['API_KEY']

class VectorDB():
    def __init__(self):
        pass

    def connect(self, service):
        connections.connect(host=f'{Milvus['HOST']}', port=Milvus['PORT'])
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
              FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
            ]
            schema = CollectionSchema(fields=fields)
            collection = Collection(name=f'{service}', schema=schema)
            collection.create_index(field_name="embedding", index_params=Milvus['INDEX_PARAM'])
            collection.load()
            return collection
        if service == 'grepp':
            # if utility.has_collection(f'{service}'):
            #     utility.drop_collection(f'{service}')
            fields = [
              FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
              FieldSchema(name='pNumber', dtype=DataType.INT64),
              FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='partTitle', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
              FieldSchema(name='level', dtype=DataType.INT64),
              FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='example', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='constraint', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='testCase', dtype=DataType.VARCHAR, max_length=64000),
            #   FieldSchema(name='output', dtype=DataType.VARCHAR, max_length=64000),
              FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
            ]
            schema = CollectionSchema(fields=fields)
            collection = Collection(name=f'{service}', schema=schema)
            collection.create_index(field_name="embedding", index_params=Milvus['INDEX_PARAM'])
            collection.load()
            return collection
    
    def embed(self, texts):
        embeddings = openai.Embedding.create(
            input=texts,
            engine=Openai['EMBED_MODEL']
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
            param=Milvus['QUERY_PARAM'],
            limit=top_k,
            output_fields= ['title', 'level',  'description', 'example', 'constraint', 'output'],
          )

        def json_default(value):
            if isinstance(value, Hit):
                return str(value)
            raise TypeError('not JSON serializable')

        result = json.dumps(response, default=json_default, indent=4)
        to_file('./query/response.log', result)
        return result

