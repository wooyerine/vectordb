import argparse, json
import openai
from lib.vecdb import *
from lib.config import Openai
from lib.logging_ import to_file

openai.api_key = Openai['API_KEY']

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help='path of dosc or text')
    parser.add_argument('--search-collection', type=str, choices=['robotics', 'robotics_overlapped'])
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = arg_parse()
    milvus = VectorDB()
    search_collection = milvus.connect_collection(args.search_collection)
    with open(f'./robotics/input/{args.query}', 'r') as f:
        text = f.read()
    result = milvus.search(collection=search_collection, data=text, target='embedding', output_fields=['id', 'description'])
    to_file(f'./robotics/result/{args.search_collection}', f'response-{args.query}.json', result, 'json')
        
