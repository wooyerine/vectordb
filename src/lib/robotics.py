import os, sys, json, argparse
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from lib.logging_ import *
from lib.vecdb import *
from lib.config import Robotics

DATA_PATH = './robotics/data/data_train_t.json'

def insert_per_page():
    milvus = VectorDB()
    collection = milvus.connect_collection(collection_name='robotics')
    array = [
        [], # description
    ]

    with open(f'{DATA_PATH}', 'r') as f:
        data = json.load(f)
    for element in data:
        array[0].append(element['content'])
    print(f"===== Start Inserting data to '{collection.name}' ===== ")
    milvus.ingest(collection=collection, data=array, embed_target=array[0])
    print(f"===== End Inserting data to '{collection.name}' ===== ")

def insert_overlapped(chunk_size=20):
    milvus = VectorDB()
    collection = milvus.connect_collection(collection_name=f'robotics_overlapped_{Robotics["CHUNK_SIZE"]}')
    document = ''
    array = [
        [], # description
    ]
    with open(f'{DATA_PATH}', 'r') as f:
        data = json.load(f)
    for element in data:
        document = document + element['content']
    words = document.split()

    # 오버래핑 부분의 길이
    overlap_length = chunk_size

    # 각 파트의 길이 (총 단어 수 / 5를 하고 오버래핑 길이만큼 더해줌)
    part_length = len(words) // chunk_size + overlap_length

    # 5개의 파트를 생성
    for i in range(chunk_size):
        start_index = i * (part_length - overlap_length)
        end_index = start_index + part_length
        part = words[start_index:end_index]
        array[0].append(" ".join(part))

    print(f"===== Start Inserting data to '{collection.name}' ===== ")
    milvus.ingest(collection=collection, data=array, embed_target=array[0])
    print(f"===== End Inserting data to '{collection.name}' ===== ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--overlap', default=False, type=bool)
    args = parser.parse_args()
    if args.overlap == False:
        insert_per_page()
    if args.overlap == True:
        insert_overlapped(chunk_size=Robotics["CHUNK_SIZE"])
    