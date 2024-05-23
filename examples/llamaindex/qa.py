import argparse
import openai
from vecdb import *
from grepp import *
from leetcode import *

openai.api_key = ""

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', type=str, choices=['leetcode', 'grepp'])
    parser.add_argument('--language', default='python3', type=str)
    parser.add_argument('--query', type=int, help='how many problems to ingest')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = arg_parse()
    milvus = VectorDB()

    collection = milvus.connect(args.service)
    if args.service == 'leetcode':
        leetcode = Leetcode()
        code = leetcode.get_problem([args.query], args.language)[3]
        result = milvus.query(collection=collection, query=code)
        print(result)
    if args.service == 'grepp':
        grepp = Grepp()
