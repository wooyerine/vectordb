import requests, json, argparse, os, sys
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
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

def insert_problem_info(path, volume):
    milvus = VectorDB()
    collection = milvus.connect_collection(collection_name="grepp")
    
    for i in tqdm(range(volume)):
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
        print(f"===== Start Inserting data to '{collection.name}' ===== ")
        milvus.ingest(collection=collection, data=array, embed_target=array[5])
        print(f"===== End Inserting data to '{collection.name}' ===== ")
    
def insert_problem_solution(path, volume):
    milvus = VectorDB()
    collection = milvus.connect_collection(collection_name="grepp_solution")
    
    for i in tqdm(range(volume)):
        array = [
            [], # 0 challenge_id
            [], # 1 solution_id
            [], # 2 code
        ]
        with open(f'{path}/{i}.json', 'r') as f:
            json_data = json.load(f)

        problems = json_data['challenges']
        print(len(problems))
        # Initialize separate lists for ids, challengeIds, and codes

        # Filter solutionGroups by language 'python3' for each problem
        for problem in problems:
            for solution_group in problem['solutionGroups']:
                if solution_group['language'] == 'python3':
                    array[0].append(solution_group['challengeId'])
                    array[1].append(solution_group['id'])
                    array[2].append(solution_group['code'])
        print(f"===== Start Inserting data to '{collection.name}' ===== ")
        milvus.ingest(collection=collection, data=array, embed_target=array[2])
        print(f"===== End Inserting data to '{collection.name}'   ===== ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract', default=False, type=bool)
    
    parser.add_argument('--insert', type=str, choices=['data', 'solution'])
    parser.add_argument('--path', required=True, type=str)
    parser.add_argument('--volume', default=11, type=int)
    args = parser.parse_args()
    
    grepp = Grepp()
    if args.extract:
        if not os.path.exists('./data/grepp'):
            grepp.list_challenges()
    if args.insert == 'data':
        insert_problem_info(args.path, args.volume)
    if args.insert == 'solution':
        insert_problem_solution(args.path, args.volume)
    
    # $ python3.10 lib/grepp.py --insert data --path ./data/grepp 
    # $ python3.10 lib/grepp.py --insert solution --path ./data/grepp 