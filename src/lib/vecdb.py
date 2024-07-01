from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import openai
import argparse, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lib.config import Milvus, Openai
from lib.fields import (
    grepp_fields, leetcode_fields, leetcode_v2_fields, robotics_fields,
    grepp_solution_fields, leetcode_solution_fields
)

openai.api_key = Openai['API_KEY']

class VectorDB():
    def __init__(self):
        pass
    
    def connect_collection(self, collection_name):
        print(f"<Collection>:\n -------------\n <Host:Port> {Milvus['HOST']}:{Milvus['PORT']}")
        connections.connect(host=Milvus['HOST'], port=Milvus['PORT'])
        collection = Collection(f"{collection_name}")      # Get an existing collection.
        collection.load()
        return collection
    
    def create_collection(self, collection_name, fields, embed_field):
        print(f"<Collection>:\n -------------\n <Host:Port> {Milvus['HOST']}:{Milvus['PORT']}")
        connections.connect(host=Milvus['HOST'], port=Milvus['PORT'])
        
        if utility.has_collection(f'{collection_name}'):
            utility.drop_collection(f'{collection_name}')
        
        schema = CollectionSchema(fields=fields, enable_dynamic_field=True)
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

    def search(self, collection, data, target, top_k=5, output_fields=['problem_id', 'title', 'level',  'description', 'examples', 'constraints']):
        result = {}
        # output_fields = ['problem_id', 'title', 'level',  'description', 'examples', 'constraints']
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
            "response": sorted(response, key=lambda x: x['distance'])
        }

        return result

if __name__ == "__main__":
    # from logging_ import to_file

    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str)
    args = parser.parse_args()
    
    milvus = VectorDB()

    if args.collection == 'grepp':
        print(f'args.collection: {args.collection}')
        grepp_collection = milvus.create_collection(collection_name='grepp', fields=grepp_fields, embed_field='desc_embedding')
    if args.collection == 'leetcode':
        print(f'args.collection: {args.collection}')
        leetcode_collection = milvus.create_collection(collection_name='leetcode', fields=leetcode_fields, embed_field='desc_embedding')
    if args.collection == 'leetcode_v2':
        print(f'args.collection: {args.collection}')
        leetcode_collection = milvus.create_collection(collection_name='leetcode_v2', fields=leetcode_v2_fields, embed_field='embedding')
    
    if args.collection == 'grepp_solution':
        print(f'args.collection: {args.collection}')
        collection = milvus.create_collection(collection_name='grepp_solution', fields=grepp_solution_fields, embed_field='code_embedding')
    if args.collection == 'leetcode_solution':
        print(f'args.collection: {args.collection}')
        collection = milvus.create_collection(collection_name='leetcode_solution', fields=leetcode_solution_fields, embed_field='code_embedding')
        
    if args.collection == 'robotics':
        print(f'args.collection: {args.collection}')
        collection = milvus.create_collection(collection_name='robotics', fields=robotics_fields, embed_field='embedding')
        print(collection)
    
    if args.collection == 'robotics-overlapped':
        print(f'args.collection: {args.collection}')
        collection = milvus.create_collection(collection_name='robotics_overlapped', fields=robotics_fields, embed_field='embedding')
        print(collection)