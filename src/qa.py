import argparse, json
import openai
from lib.vecdb import *
from lib.grepp import *
from lib.leetcode import *
from lib.config import Openai

openai.api_key = Openai['API_KEY']

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help='path of dosc or text')
    # parser.add_argument('--service', type=str, choices=['leetcode', 'grepp'])
    parser.add_argument('--search-collection', type=str, choices=['leetcode', 'grepp', 'leetcode_v2'])
    parser.add_argument('--language', default='python3', type=str)
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = arg_parse()
    milvus = VectorDB()
    leetcode = Leetcode()
    search_collection = milvus.connect_collection(args.search_collection)
    
    # if args.service == 'leetcode':
    #     collection = milvus.connect_collection("leetcode")
    #     leetcode = Leetcode()
    #     problem = json.loads(leetcode.get_problem(args.query, args.language, './result/query/leetcode'))
    #     result = milvus.search(collection=search_collection, data=problem["description"], target='desc_embedding')
    #     to_file('./result/query/leetcode', f'response-{args.query}.json', result, 'json')
    # if args.service == 'grepp':
    #     collection = milvus.connect_collection("grepp")
    #     grepp = Grepp()
    #     problem = milvus.query(collection=collection, expr=f'title == "{args.query}"')
    #     result = milvus.search(collection=search_collection, data=problem[0]["description"], target='desc_embedding')
    #     to_file('./result/query/grepp', f'response-{args.query}.json', result, 'json')
    with open(f'{args.query}', 'r') as f:
        text = f.read()
    if args.search_collection == 'leetcode_v2':
        target = 'embedding'
    else:
        target = 'desc_embedding'
    result = milvus.search(collection=search_collection, data=text, target=target)
    to_file(f'./result/query/{args.search_collection}', f'response-{args.query}.json', result, 'json')
