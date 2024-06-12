import argparse, json
import openai
from lib.vecdb import *
from lib.grepp import *
from lib.leetcode import *
from lib.config import Openai

openai.api_key = Openai['API_KEY']

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', type=str, choices=['leetcode', 'grepp'])
    parser.add_argument('--language', default='python3', type=str)
    parser.add_argument('--query', type=str, help='problem id of leetcode or problem title of grepp')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = arg_parse()
    milvus = VectorDB()

    collection = milvus.connect_collection(args.service)
    if args.service == 'leetcode':
        leetcode = Leetcode()
        problem = json.loads(leetcode.get_problem(args.query, args.language, './result/query/leetcode'))
        result = milvus.search(collection=collection, data=problem["description"], target='desc_embedding')
        to_file('./result/query/leetcode', f'response-{args.query}.json', result, 'json')
    if args.service == 'grepp':
        grepp = Grepp()
        problem = milvus.query(collection=collection, expr=f'title == "{args.query}"')
        result = milvus.search(collection=collection, data=problem[0]["description"], target='desc_embedding')
        to_file('./result/query/grepp', f'response-{args.query}.json', result, 'json')