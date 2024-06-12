from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import openai
import argparse
from lib.config import Milvus, Openai

openai.api_key = Openai['API_KEY']

class VectorDB():
    def __init__(self):
        pass
    
    def connect_collection(self, collection_name):
        connections.connect(host=Milvus['HOST'], port=Milvus['PORT'])
        collection = Collection(f"{collection_name}")      # Get an existing collection.
        collection.load()
        return collection
    
    def create_collection(self, collection_name, fields, embed_field):
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

    def query(self, collection, expr, limit=1):
        output_fields = ['problem_id', 'title', 'level',  'description', 'examples', 'constraints', 'testCases']
        result = collection.query(
            expr = expr,
            output_fields = output_fields,
            limit = limit,
        )
        return result

    def search(self, collection, data, target, top_k=6):
        result = {}
        output_fields = ['problem_id', 'title', 'level',  'description', 'examples', 'constraints']
        outputs = collection.search(
            data=self.embed(data), 
            anns_field=target, 
            param=Milvus['QUERY_PARAM'],
            limit=top_k,
            output_fields= output_fields,
          )
        response = []
        for output in outputs:
            for record in output:
                tmp = {
                    "id": record.id,
                    "distance": record.distance,
                    "entity": {}
                }
                for field in output_fields:
                    tmp["entity"].update({
                        f"{field}": record.get(field)
                    })
                response.append(tmp)
    
        result = {
            "request": {
                "collection": collection.name,
                "anns_field": target,
                "param": Milvus['QUERY_PARAM'],
                "limit": top_k,
                "output_fields": output_fields,
            },
            "response": response
        }

        return result

if __name__ == "__main__":
    # from logging_ import to_file
    from config import Milvus, Openai

    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str)
    args = parser.parse_args()
    
    milvus = VectorDB()

    leetcode_fields = [
      FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
      FieldSchema(name='problem_id', dtype=DataType.INT64),
      FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
      FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='testcases', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='source_code_name', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='code_template', dtype=DataType.VARCHAR, max_length=64000),
      FieldSchema(name='desc_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
    ]

    grepp_fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='problem_id', dtype=DataType.INT64),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='partTitle', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
        FieldSchema(name='level', dtype=DataType.INT64),
        FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='testCases', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
        FieldSchema(name='desc_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
    ]

    grepp_solution_fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='challenge_id', dtype=DataType.INT64),
        FieldSchema(name='solution_id', dtype=DataType.INT64),
        FieldSchema(name='code', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='code_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
    ]
    
    leetcode_solution_fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='problem_id', dtype=DataType.INT64),
        FieldSchema(name='solution_id', dtype=DataType.INT64),
        FieldSchema(name='code', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='code_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
    ]

    if args.collection == 'grepp':
        grepp_collection = milvus.create_collection(collection_name='grepp', fields=grepp_fields, embed_field='desc_embedding')
    if args.collection == 'leetcode':
        leetcode_collection = milvus.create_collection(collection_name='leetcode', fields=leetcode_fields, embed_field='desc_embedding')
    if args.collection == 'grepp_solution':
        collection = milvus.create_collection(collection_name='grepp_solution', fields=grepp_solution_fields, embed_field='code_embedding')
    if args.collection == 'leetcode_solution':
        collection = milvus.create_collection(collection_name='leetcode_solution', fields=leetcode_solution_fields, embed_field='code_embedding')
        