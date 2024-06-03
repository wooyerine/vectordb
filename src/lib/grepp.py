import requests, json
from tqdm import tqdm
from lib.config import Account
from lib.logging_ import to_file

class Grepp:
    def __init__(self):
        self.base = 'https://etri.programmers.co.kr/api/v1/etri'
        self.token = self.get_token()
    
    def get_token(self):
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
            to_file(f'./data/grepp/{page}.json', tmp, type='json')
    
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

    def refine_data(self):
        array = [
            [], # 0 pNumber
            [], # 1 title
            [], # 2 partTitle
            [], # 3 languages
            [], # 4 level 
            [], # 5 description
            [], # 6 example
            [], # 7 constraint
            [], # 8 testcases
            [], # 9 solution-python
        ]
        for i in range(11):
            with open(f'{i}_20240530-*.json', 'r') as f:
                json_data = json.load(f)
            # print(json_data)
            problems = json_data['challenges']
            print(len(problems))