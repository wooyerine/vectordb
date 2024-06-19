import subprocess, time, re, os, argparse, json, sys
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from lib.logging_ import to_file, save_json_in_chunks
from lib.vecdb import *

FILE_PATH = "./data/leetcode"

class Leetcode:
  def __init__(self) -> None:
    pass

  def get_problem(self, id, language, path):
    if not os.path.exists(f'{path}/leetcode-source-file'):
      os.makedirs(f'{path}/leetcode-source-file')
    
    raw = subprocess.run(
          f"leetcode show {id} -g -x -o {path}/leetcode-source-file -l {language}", 
          shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
      ).stdout.decode("utf-8")
    time.sleep(3)
    # Remove ANSI color codes
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    raw_cleaned = ansi_escape.sub('', raw)

    # Split the cleaned raw text into lines
    lines = raw_cleaned.split('\n')
    
    # Extract problem_id and title
    try:
      problem_id = int(lines[0].split(']')[0][1:])
      title = lines[0].split('] ')[1].strip()
    except (IndexError, ValueError) as e:
      print(e)
      problem_id = ''
      title = ''

    # Extract languages
    try:
      languages_line = next(line for line in lines if line.startswith("Langs:"))
      languages = languages_line.split(":")[1].strip().split()
    except:
      languages = ''

    # Extract level
    try:
      level_line = next(line for line in lines if line.startswith("* Easy") or line.startswith("* Medium") or line.startswith("* Hard"))
      level = level_line.split(' ')[1].strip()
    except:
      level = ''

    # Extract source_code_name
    try:
      source_code_line = next(line for line in lines if line.startswith("* Source Code:"))
      code_name = source_code_line.split(":")[1].strip()
    except:
      code_name = ''
    if len(code_name) > 0:
      source_code_name = os.path.basename(code_name)
    else:
      source_code_name = ''

    # Extract testcases
    try:
      testcases_line = next(line for line in lines if line.startswith('* Testcase Example:'))
      testcases = testcases_line.strip()
      testcases_index = lines.index(testcases_line)
    except:
      testcases = ''
      testcases_index = -1

    # Extract description
    try:
      examples_start_index = next(i for i, line in enumerate(lines) if re.match(r'Example ?\d*:', line))
    except:
      examples_start_index = testcases_index + 1

    description = '\n'.join(lines[testcases_index+1:examples_start_index]).strip()

    # Extract examples
    try:
      examples_end_index = lines.index('Constraints:')
      examples = '\n'.join(lines[examples_start_index:examples_end_index]).strip()
    except ValueError:
      examples = ''

    # Extract constraints
    try:
      constraints_start_index = lines.index('Constraints:')
      constraints = '\n'.join(lines[constraints_start_index:]).strip()
    except ValueError:
      constraints = ''
    
    code_template = subprocess.run(
          f"leetcode show {id} -c -l {language}", 
          shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
      ).stdout.decode("utf-8")

    time.sleep(3)
    # Create the JSON structure
    leetcode = {
        "problem_id": problem_id,
        "title": title,
        "languages": languages,
        "level": level,
        "description": description,
        "examples": examples,
        "constraints": constraints,
        "testcases": testcases,
        "source_code_name": source_code_name,
        "code_template": code_template,
    }

    # Output the JSON structure
    json_data = json.dumps(leetcode, indent=2)
    return json_data

  def get_problems_with_level(self, language, level):
    path = f'{FILE_PATH}/{level}'
    leetcode = {
      "page": 0,
      "limit": 50,
      "problems": []
    }
    raw = subprocess.run(f"leetcode list -q {level}L -t algorithms", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
    
    raw_list = raw.split("\n")
    problem_list = []
    # Loop through each string in the raw_list
    for item in raw_list:
      # Use regex to find the number inside the square brackets
      match = re.search(r'\[\s*(\d+)\s*\]', item)
      if match:
        # Append the found number to the problem_list
        problem_list.append(int(match.group(1)))
    print(problem_list)
    for index in tqdm(range(len(problem_list))):  
      print(problem_list[index])
      json_data = self.get_problem(problem_list[index], language, path)
      leetcode["problems"].append(json.loads(json_data))
      if (index + 1) % 50 == 0:
        to_file(directory=path, file_name=f'{leetcode["page"]}.json', data=leetcode, data_type='json')
        leetcode["page"] += 1
        leetcode["problems"] = []
    if leetcode["problems"]:
      to_file(directory=path, file_name=f'{leetcode["page"]}.json', data=leetcode, data_type='json')

  def get_topics(self):
    # ANSI 이스케이프 시퀀스를 제거하는 함수
    def remove_ansi_escape_sequences(text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)

    # 자물쇠 없는 문제 추출 함수
    def extract_problems(data, topic):
        problems = []
        for item in data.strip().split('\n'):
            if '\U0001F512' not in item:
                problem_id_start = item.find('[') + 1
                problem_id_end = item.find(']')
                problem_id = item[problem_id_start:problem_id_end].strip()

                # 제목과 난이도 추출
                title_level = item[problem_id_end + 1:].strip().rsplit('  ', 1)
                if len(title_level) < 2:
                    continue  # 제목과 난이도가 모두 있는 항목만 처리
                title = title_level[0].strip()
                level = remove_ansi_escape_sequences(title_level[1]).strip()
                
                problems.append({
                    "problem_id": problem_id,
                    "title": title,
                    "level": level,
                    "topic": [topic]
                })
        return problems
    topics = [
      "array", "string", "hash-table", "dynamic-programming", "math", 
      "sorting", "greedy","depth-first-search", "binary-search",
      "tree", "Breadth-first-search", "matrix", "bit-manipulation", "two-pointers",
      "binary-tree", "heap-priority-queue", "prefix-sum", "stack", "simulation",
      "graph", "counting", "design", "sliding-window", "backtracking",
      "enumeration", "union-find", "linked-list", "ordered-set", "monotonic-stack",
      "number-theory", "trie", "divide-and-conquer", "bitmask", "recursion",
      "queue", "segment-tree", "binary-search-tree", "memoization", "geometry",
      "binary-indexed-tree", "hash-function", "combinatorics", "topological-sort", "string-matching",
      "shortest-path", "rolling-hash", "game-theory", "interactive", "data-stream",
      "brainteaser", "monotonic-queue", "randomized", "merge-sort", "iterator",
      "concurrency", "doubly-linked-list", "probability-and-statistics", "quickselect", "bucket-sort",
      "suffix-array", "minimum-spanning-tree", "counting-sort", "shell", "line-sweep",
      "reservoir-sampling", "strongly-connected-component", "eulerian-circuit", "radix-sort", "rejection-sampling",
      "biconnected-component"
    ]
    
    variables = []
    for topic in tqdm(topics):
        print(f"======== {topic} ========")
        raw = subprocess.run(
                f"leetup list --tag {topic}", 
                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
        time.sleep(3)
        variables.append((f"{topic}", raw))
    # 모든 변수를 처리하여 자물쇠 없는 문제 추출
    all_problems = []
    for variable_name, variable_data in tqdm(variables):
        topic = variable_name  # 변수 이름을 토픽으로 사용
        print(f"======== {topic} ========")
        problems = extract_problems(variable_data, topic)
        all_problems.extend(problems)
    # 문제 번호를 기준으로 합치기
    combined_problems = {}
    for problem in all_problems:
        problem_id = problem["problem_id"]
        if problem_id in combined_problems:
            combined_problems[problem_id]["topic"].append(problem["topic"][0])
        else:
            combined_problems[problem_id] = problem

    # JSON 형태로 출력
    combined_problems_list = list(combined_problems.values())
    # JSON 데이터를 50개씩 쪼개서 저장
    save_json_in_chunks(combined_problems_list, 100)
    return combined_problems_list

def insert_problem_info(path, volume):
  milvus = VectorDB()
  collection = milvus.connect_collection(collection_name="leetcode")

  for i in tqdm(range(volume)):
    array = [
        [], # 0 problem_id
        [], # 1 title
        [], # 2 languages
        [], # 3 level
        [], # 4 description 
        [], # 5 examples
        [], # 6 constraints
        [], # 7 testcases
        [], # 8 source_code_name
        [], # 9 code_template
    ]
    with open(f'{path}/{i}.json', 'r') as f:
        json_data = json.load(f)
    # print(json_data)
    problems = json_data['problems']
    print(len(problems))
    for j in tqdm(range(len(problems))):
        array[0].append(problems[j]['problem_id'])
        array[1].append(problems[j]['title'])
        array[2].append(problems[j]['languages'])
        array[3].append(problems[j]['level'])
        array[4].append(problems[j]['description'])
        array[5].append(problems[j]['examples'])
        array[6].append(problems[j]['constraints'])
        array[7].append(problems[j]['testcases'])
        array[8].append(problems[j]['source_code_name'])
        array[9].append(problems[j]['code_template'])
    print(f"===== Start Inserting data to '{collection.name}' ===== ")
    milvus.ingest(collection=collection, data=array, embed_target=array[4])
    print(f"===== End Inserting data to '{collection.name}' ===== ")
    
def insert_problem_info_v2(path, volume):
    milvus = VectorDB()
    collection = milvus.connect_collection(collection_name="leetcode_v2")
    with open('./data/leetcode/topic.json', 'r') as f:
      file_data = json.load(f)
    def topics(problem_id, data):
      for problem in data:
        if problem["problem_id"] == str(problem_id):
            return problem["topic"]
      return ['']
    
    for i in tqdm(range(volume)):
      tmp = [
          [], # 0 problem_id
          [], # 1 title
          [], # 2 topic
          [], # 3 languages
          [], # 4 level
          [], # 5 description 
          [], # 6 examples
          [], # 7 constraints
          [], # 8 testcases
          [], # 9 code_template
          [], # 10 for embedding
      ]
      with open(f'{path}/{i}.json', 'r') as f:
          json_data = json.load(f)
      # print(json_data)
      problems = json_data['problems']
      print(len(problems))

      for j in tqdm(range(len(problems))):
          print(f"===== Processing: '{problems[j]['problem_id']}' ===== ")
          topic_data = topics(problems[j]['problem_id'], file_data)

          topics_sum = ''
          for topic in topic_data:
              topics_sum = topics_sum + topic
          tmp[0].append(problems[j]['problem_id'])
          tmp[1].append(problems[j]['title'])
          tmp[2].append(topic_data)
          tmp[3].append(problems[j]['languages'])
          tmp[4].append(problems[j]['level'])
          tmp[5].append(problems[j]['description'])
          tmp[6].append(problems[j]['examples'])
          tmp[7].append(problems[j]['constraints'])
          tmp[8].append(problems[j]['testcases'])
          tmp[9].append(problems[j]['code_template'])
          tmp[10].append(topics_sum+problems[j]['description']+problems[j]['examples']+problems[j]['constraints']+problems[j]['code_template'])
      print(f"===== Start Inserting data to '{collection.name}' ===== ")
      array = tmp[:10]
      print(len(array))
      milvus.ingest(collection=collection, data=array, embed_target=tmp[10])
      print(f"===== End Inserting data to '{collection.name}' ===== ")

def insert_problem_solution(path, volume):
    milvus = VectorDB()

    for i in tqdm(range(volume)):
        array = [
            [], # 0 problem_id
            [], # 1 solution_id
            [], # 2 code
        ]
        with open(f'{path}/{i}.json', 'r') as f:
            json_data = json.load(f)
        problems = json_data['problems']
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
  parser.add_argument('--topic', default=False, type=bool)
  parser.add_argument('--extract', default=False, type=bool)
  parser.add_argument('--level', type=str)
  parser.add_argument('--insert', type=str, choices=['data', 'solution'])
  parser.add_argument('--path', type=str)
  parser.add_argument('--volume', type=int)
  args = parser.parse_args()

  leetcode = Leetcode()
  if args.topic:
    problem_topics = leetcode.get_topics()
  if args.extract:
    if args.level == 'e':
      if not os.path.exists('./data/leetcode/e'):
        os.makedirs('./data/leetcode/e')
      leetcode.get_problems_with_level('python3', 'e')
    if args.level == 'm':
      if not os.path.exists('./data/leetcode/m'):
        os.makedirs('./data/leetcode/m')
      leetcode.get_problems_with_level('python3', 'm')
    if args.level == 'h':
      if not os.path.exists('./data/leetcode/h'):
        os.makedirs('./data/leetcode/h')
      leetcode.get_problems_with_level('python3', 'h')

  if args.insert == 'data':
    # insert_problem_info(args.path, args.volume)
    insert_problem_info_v2(args.path, args.volume)
  if args.insert == 'solution':
    insert_problem_solution(args.path, args.volume)

# $ python3.10 lib/leetcode.py --insert data --path ./data/leetcode/{e, m, h}
# $ python3.10 lib/leetcode.py --insert solution --path ./data/leetcode/solution/{e, m, h}