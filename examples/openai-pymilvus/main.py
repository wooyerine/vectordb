from config import Milvus, Openai, Data
from pymilvus import connections, utility, FieldSchema, Collection, CollectionSchema, DataType
import openai
import datasets
from tqdm import tqdm
import textwrap

def set_milvus(collection_name):
    # Connect to Milvus Database
    connections.connect(host=Milvus["HOST"], port=Milvus["PORT"])

    # Remove collection if it already exists
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    # Create collection which includes the id, title, and embedding.
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='type', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='release_year', dtype=DataType.INT64),
        FieldSchema(name='rating', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus["DIMENSION"])
    ]
    schema = CollectionSchema(fields=fields)
    collection = Collection(name=collection_name, schema=schema)

    # Create the index on the collection and load it.
    collection.create_index(field_name="embedding", index_params=Milvus["INDEX_PARAM"])
    collection.load()
    return collection

# Simple function that converts the texts to embeddings
def embed(texts):
    embeddings = openai.Embedding.create(
        input=texts,
        engine=Openai["OPENAI_ENGINE"]
    )
    return [x['embedding'] for x in embeddings['data']]

def insert_data(data_name, collection):
    # Download the dataset 
    dataset = datasets.load_dataset(data_name, split='train')
    # [참고사항]
    # - 'hugginglearners/netflix-shows' 데이터는 총 8807 rows로 모두 embedding 시키는데 11분 정도 소요.
    # - len(dataset) --> 작은 숫자로 변경 시 소요시간 단축

    entity = [
        [], # 0 title
        [], # 1 type
        [], # 2 release_year
        [], # 3 rating
        [], # 4 description
    ]

    # Embed and insert in batches
    for i in tqdm(range(0, len(dataset))):
    # for i in tqdm(range(0, 10)):
        entity[0].append(dataset[i]['title'] or '')
        entity[1].append(dataset[i]['type'] or '')
        entity[2].append(dataset[i]['release_year'] or -1)
        entity[3].append(dataset[i]['rating'] or '')
        entity[4].append(dataset[i]['description'] or '')
        if len(entity[0]) % Openai["BATCH_SIZE"] == 0:
            # embedding "description"
            # if embedding other field --> change entity[index]
            entity.append(embed(entity[4]))
            collection.insert(entity)
            entity = [[],[],[],[],[]]
    
    print('=== Success Entity Embed and Insert to Milvus ===')

def query(collection, query, top_k = 5):
    text, expr = query
    res = collection.search(embed(text), anns_field='embedding', expr = expr, param=Milvus["QUERY_PARAM"], limit = top_k, output_fields=['title', 'type', 'release_year', 'rating', 'description'])
    for i, hit in enumerate(res):
        print('Description:', text, 'Expression:', expr)
        print('Results:')
        for ii, hits in enumerate(hit):
            print('\t' + 'Rank:', ii + 1, 'Score:', hits.score, 'Title:', hits.entity.get('title'))
            print('\t\t' + 'Type:', hits.entity.get('type'), 'Release Year:', hits.entity.get('release_year'), 'Rating:', hits.entity.get('rating'))
            print(textwrap.fill(hits.entity.get('description'), 88))
            print()

if __name__ == '__main__':
    openai.api_key = Openai['API_KEY']
    collection = set_milvus(collection_name='movie_search')
    # Choose Entity index to embed_target for vector embedding
    insert_data(data_name=Data['netflix-shows'], collection=collection)
    
    my_query = ('movie about a fluffly animal', 'release_year < 2019 and rating like \"PG%\"')
    query(collection=collection, query=my_query)



