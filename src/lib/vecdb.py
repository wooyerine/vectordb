from pymilvus import (
    Hit,
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import openai
import json
from lib.logging_ import to_file
from lib.config import Milvus, Openai

openai.api_key = Openai['API_KEY']

class VectorDB():
    def __init__(self):
        pass

    def connect(self, collection_name, fields, embed_field):
        connections.connect(host=Milvus['HOST'], port=Milvus['PORT'])
        
        if utility.has_collection(f'{collection_name}'):
            utility.drop_collection(f'{collection_name}')
        
        schema = CollectionSchema(fields=fields)
        collection = Collection(name=f'{collection_name}', schema=schema)
        collection.create_index(field_name=f"{embed_field}", index_params=Milvus['INDEX_PARAM'])
        collection.load()
        return collection
    
    def embed(self, texts):
        embeddings = openai.Embedding.create(
            input=texts,
            engine=Openai['EMBED_MODEL']
        )
        return [x['embedding'] for x in embeddings['data']]
    
    def ingest(self, collection, data, embed_target):
        data.append(self.embed(embed_target))
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

# fields = [
#     FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
#     FieldSchema(name='pNumber', dtype=DataType.INT64),
#     FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='example', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='constraint', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='output', dtype=DataType.VARCHAR, max_length=64000),
#     FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
# ]
