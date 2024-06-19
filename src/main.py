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
    print('')
