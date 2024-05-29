import argparse, os
from lib.leetcode import *
from lib.grepp import *
from lib.vecdb import *
import openai
# from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,PromptTemplate
# from llama_index.vector_stores.milvus import MilvusVectorStore

MODEL = 'gpt-3.5-turbo'
RESULT_PATH = './query/result.txt'

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', type=str, choices=['leetcode', 'grepp'])
    parser.add_argument('--number', nargs='+', type=int, help='"problem_number, problem_number, ..."')
    parser.add_argument('--level', nargs='*', type=str, choices=['h', 'm', 'e', 'all'])
    parser.add_argument('--language', default='python3', type=str)
    parser.add_argument('--volume', type=int, help='how many problems to ingest')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = arg_parse()
    milvus = VectorDB()
    collection = milvus.connect(args.service)
    if args.service == 'leetcode':
        leetcode = Leetcode()
        if args.number:
            problem = leetcode.get_problem(args.number, args.language)
            milvus.ingest(collection=collection, data=problem)
        if args.level:
            problems = leetcode.get_problems_with_level(args.language, args.level, args.volume)
            milvus.ingest(collection=collection, data=problems)
    if args.service == 'grepp':
        grepp = Grepp()
        print('make grepp instance')
        # if not os.path.exists('../data/grepp.json'):
    #     grepp.list_challenges(args.language)
        problems = grepp.refine_data('../data/grepp_20240528-162405.json')
        # milvus.ingest(collection=collection, data=problems)
        
    # vector_store = MilvusVectorStore(
    #     host = "localhost",
    #     port = "19530",
    #     collection_name = "leetcode"
    #   )
    
    # index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    # query_engine = index.as_query_engine()
    
    # response = query_engine.query("Find data about Array")
    
    # completion = openai.ChatCompletion.create(
    #   model=MODEL,
    #   messages=prompt,
    #   max_tokens=1024
    # )
    
    
    
  
