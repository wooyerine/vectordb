from milvus import *
from data.data import *
import json

if __name__ == '__main__':
  dataset = get_codes(size=1)
  collection = create_collection(collection_name='leetcode')
  insert_data(dataset=dataset, collection=collection)
    