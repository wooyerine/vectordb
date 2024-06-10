import requests, json
from tqdm import tqdm
from lib.config import Account, Milvus
from lib.logging_ import to_file
from lib.vecdb import *

class Grepp:
    def __init__(self):
        pass
    
    def get_token(self):
        self.base = 'https://etri.programmers.co.kr/api/v1/etri'
        self.token = self.get_token()
        try:
            response = requests.post(f'{self.base}/login', json={'email':Account['EMAIL'], 'password':Account["PW"]},)
        except SystemError:
            print(f'{response}')
        return response.json()['token']
    
    def list_challenges(self):
        PER_PAGE = 50
        # PER_PAGE = 2
        print(self.token)
        response = requests.get(
            f'{self.base}/challenges', 
            headers= {
                'Authorization': f'Bearer {self.token}',
                'Content-type': 'application/json',
            },
            params={
                'per_page': PER_PAGE
            }
        ).json()
        challenges = []
        for page in tqdm(range(response['totalPages'])):
        # for page in range(2):
            tmp = requests.get(
                        f'{self.base}/challenges', 
                        headers= {
                            'Authorization': f'Bearer {self.token}',
                            'Content-type': 'application/json',
                        },
                        params= {
                            'page': page+1,
                            'perPage': PER_PAGE,
                        }
                    ).json()
            for i in tqdm(range(len(tmp['challenges']))):
                print(tmp['challenges'][i]['id'])
                detail = self.get_challenge(tmp['challenges'][i]['id'])
                solutions = self.get_solution_groups(tmp["challenges"][i]['id'])
                # print(solutions)
                tmp['challenges'][i].update(detail)
                tmp['challenges'][i].update(solutions)
            to_file('./data/grepp', f'{page}.json', tmp, data_type='json')
    
    def get_challenge(self, id): # 
        response = requests.get(
            f'{self.base}/challenges/{id}', 
            headers= {
                'Authorization': f'Bearer {self.token}',
                'Content-type': 'application/json',
            },
        ).json()
        try:
            del response['id']
        except KeyError:
            print('Key "id" does not exist in the response')
        
        return response

    def get_solution_groups(self, id):
        solutions = {}
        response = requests.get(
            f'{self.base}/challenges/{id}/solution-groups', 
            headers= {
                'Authorization': f'Bearer {self.token}',
                'Content-type': 'application/json',
            },
        ).json()
        
        try:
            solutions["solutionGroups"] = response["solutionGroups"]
        except KeyError:
            print('Key "solutionGroups" does not exist in the response')
        return solutions

def refine_data(path):
    from pymilvus import (
        FieldSchema, DataType
    )
    milvus = VectorDB()

    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='problem_id', dtype=DataType.INT64),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='partTitle', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
        FieldSchema(name='level', dtype=DataType.INT64),
        FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
        FieldSchema(name='testCases', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
        FieldSchema(name='desc_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
    ]

    collection = milvus.connect(collection_name='grepp', fields=fields, embed_field='desc_embedding')
    
    for i in tqdm(range(11)):
        array = [
            [], # 0 problem_id
            [], # 1 title
            [], # 2 partTitle
            [], # 3 languages
            [], # 4 level 
            [], # 5 description
            [], # 6 example
            [], # 7 constraint
            [], # 8 testcases
        ]
        with open(f'{path}/{i}.json', 'r') as f:
            json_data = json.load(f)
        # print(json_data)
        problems = json_data['challenges']
        print(len(problems))
        for j in tqdm(range(len(problems))):
            # constrinats, example, description extraction
            full_text = problems[j]['description']
            part_limits = ["##### 제한사항", "##### 입출력 예"]
            splits = [full_text.find(part) for part in part_limits]
            description_part = full_text[:splits[0]].strip()
            constraints_part = full_text[splits[0]:splits[1]].strip()
            example_part = full_text[splits[1]:].strip()

            # testcases: convert object to string
            testcases = problems[j]['testcases']
            stringed = [str(item) for item in testcases]

            array[0].append(problems[j]['id'])
            array[1].append(problems[j]['title'])
            array[2].append(problems[j]['partTitle'])
            array[3].append(problems[j]['languages'])
            array[4].append(problems[j]['level'])
            array[5].append(description_part)
            array[6].append(example_part)
            array[7].append(constraints_part)
            array[8].append(stringed)
        milvus.ingest(collection=collection, data=array, embed_target=array[5])
    
