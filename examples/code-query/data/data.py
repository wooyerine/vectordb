import time, subprocess, re, json, os
from tqdm import tqdm

FILE_PATH = "./data/data.json"
SOURCE_PATH = './data/leetcode-source-file'

def get_code_list(level, n_sample, data):
    result = subprocess.run(f"leetcode list -q {level}L -s", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
    time.sleep(10)
    raw = result.split("\n")
    problem_list = []
    problem_number = re.compile('\[([^]]+)\]')

    print('=== Start List-Up Leetcode Problems . . . ===')
    for i in range(n_sample):
        data[0].append(level)
        problem_list.append(int(problem_number.findall(raw[i])[0]))
    print('=== End List-Up ===')
    return problem_list, data

def get_problem_detail(list, data):
    desc = ''
    example = ''
    constraint = ''
    output = ''

    for n in tqdm(range(len(list))):
        print('=== Start Getting Details . . . ===')
        result = subprocess.run(f"leetcode show {list[n]} -g -x -o {SOURCE_PATH} -l python3", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
        document = result.split('\n')
        data[1].append(document[0])

        desc_index = [i for i in range(len(document)) if '* Testcase Example:  ' in document[i]]
        example_index = [i for i in range(len(document)) if 'Example ' in document[i]]
        constraint_index = [i for i in range(len(document)) if 'Constraints:' in document[i]]
        
        for i in range(desc_index[0]+1, len(document)):
            desc += document[i]
        data[2].append(desc)
        desc = ''
        
        for i in range(example_index[0], constraint_index[0]-1):
            example += document[i]
        data[3].append(example)
        example = ''
        
        for i in range(constraint_index[0], len(document)):
            constraint += document[i]
        data[4].append(constraint)
        constraint = ''

        output_code_index = [i for i in range(len(document)) if '* Source Code:       ' in document[i]]
        source_file = document[output_code_index[0]]
        code_name = source_file[source_file.find(str(list[n])):source_file.find('.py')+3]
        # print(code_name)
        with open (f'{SOURCE_PATH}/{code_name}', "r") as f:
            lines = f.readlines()
            for line in lines:
                if '#' not in line:
                    output += line
                else:
                    continue
        data[5].append(output)
        output=''
    
    return data

def get_codes(size=3):

    data = [
        [], # 0 level
        [], # 1 pNumber (problem number)
        [], # 2 category
        [], # 3 title
        [], # 4 description
        [], # 5 example
        [], # 6 constraints
        [], # 7 output template
        [], # 8 answer
    ]
    level = {
        'hard': 'h',
        'medium': 'm',
        'easy': 'e'
    }

    print('=== Start Loading Data . . . ===')
    if os.path.isfile(FILE_PATH):
        print('=== File Exists ===')
        with open(FILE_PATH) as f:
            json_data = json.load(f)
        print(json_data)
        for i in range(len(json_data['level'])):
            data[0].append(json_data['level'][i])
            data[1].append(json_data['pNumber'][i])
            data[2].append(json_data['category'][i])
            data[3].append(json_data['title'][i])
            data[4].append(json_data['description'][i])
            data[5].append(json_data['example'][i])
            data[6].append(json_data['constraints'][i])
            data[7].append(json_data['output'][i])
            data[8].append(json_data['answer'][i])
        print('=== End Loading Data ===')
        return data
    else:
        for l in level:
            print(f'=== Start Level: {level[l]} ===')
            problem_list, data = get_code_list(level=level[l], n_sample=size, data=data)
            data = get_problem_detail(list=problem_list, data=data)
        with open("./data/data.json", "w") as json_file:
            tmp = {
                'level': data[0],
                'pNumber': data[1],
                'title': data[1],
                'description': data[2],
                'example': data[3],
                'constraints': data[4],
                'output': data[5],
            }
            json.dump(tmp, json_file)
        
        print('=== End Loading Data ===')
        return data
    
