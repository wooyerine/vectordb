import subprocess

EMAIL = 'etri-test@grepp.co'
PW = '0isfha0!_F__FD12'

class Grepp:
    def __init__(self) -> None:
        self.base = 'https://etri.programmers.co.kr/api/v1/etri/'
    
    def session(self):
        cmd = f"""
                    curl -X 'GET' '{self.base}/login' \
                    -H 'accept: application/json' \
                    -H 'Content-Type: application/json' \
                    -d '{
                        "email": {EMAIL},
                        "password": {PW}
                    }'
                """
        token = subprocess.run(
            cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
                               ).stdout.decode("utf-8")
        return token

    def list_challenges(self, level, language, volume):
        token = self.session()
        print(token)
        cmd = f"""
                curl -X 'GET' \
                '{self.base}challenges?languages%5B%5D={language}&levels%5B%5D={level}&page=1&per_page={volume}' \
                -H 'accept: application/json'\
                -H 'Authorization: Bearer {token}'
            """
        response = subprocess.run(
            cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
                                    ).stdout.decode("utf-8")
        print(response)
        problem_list = []
        for i in range(len(response.challenges)):
            print()
        
    
    def get_challenge(self, id): # 
        array = [
          [], # 0 pNumber
          [], # 1 title
          [], # 2 level
          [], # 3 description
          [], # 4 example 
          [], # 5 constraint
          [], # 6 output
        ]
        print()

    def get_solution_groups():
        print()