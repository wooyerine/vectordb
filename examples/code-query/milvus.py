from config import Milvus, Openai, Data
from pymilvus import connections, utility, FieldSchema, Collection, CollectionSchema, DataType
import openai
from data.data import *

openai.api_key = ""

def create_collection(collection_name):
    # Connect to Milvus Database
    print(f'=== Start Connect to {Milvus["HOST"]}:{Milvus["PORT"]} . . . ===')
    connections.connect(host=Milvus["HOST"], port=Milvus["PORT"])

    # Remove collection if it already exists
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
        
    # else:
    # Create collection which includes the id, title, and embedding.
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='pNumber', dtype=DataType.INT64),
        FieldSchema(name='category', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='example', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='output', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='answer', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='descEmbedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus["DIMENSION"]),
        FieldSchema(name='answerEmbedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus["DIMENSION"]),
    ]
    schema = CollectionSchema(fields=fields)
    collection = Collection(name=collection_name, schema=schema)

    # Create the index on the collection and load it.
    collection.create_index(field_name="descEmbedding", index_params=Milvus["INDEX_PARAM"])
    collection.create_index(field_name="answerEmbedding", index_params=Milvus["INDEX_PARAM"])
    collection.load()
    return collection

# Simple function that converts the texts to embeddings
def embed(texts):
    embeddings = openai.Embedding.create(
        input=texts,
        engine='text-embedding-3-small'
    )
    return [x['embedding'] for x in embeddings['data']]

def insert_data(dataset, collection):
    print('=== Start Embedding Target: description . . . ===')

    dataset.append(embed(dataset[4]))
    dataset.append(embed(dataset[8]))
    print('=== End Embedding ===')

    print('=== Start Inserting to Collection . . . ===')
    collection.insert(dataset)
    print('=== End Inserting ===')
    
    print('=== Success Entity Embed and Insert to Milvus ===')
