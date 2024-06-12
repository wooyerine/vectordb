import subprocess, time, re, os, argparse, json, sys
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from lib.logging_ import to_file
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

  def get_topics(self, language, level):
    topics = [
      "array", "string", "hash-table", "dynamic-programming", "math", 
      "sorting", "greedy", "depth-first-search", "binary-search",
      "tree", "breadth-first-search", "matrix", "bit-manipulation", "two-pointers",
      "binary-tree", "heap-priority-queue", "prefix-sum", "stack", "simulation",
      "graph", "counting", "design", "sliding-window", "backtracking",
      "enumeration", "union-find", "linked-list", "ordered-set", "monotonic-stack",
      "number-theory", "trie", "divide-and-conquer", "bitmask", "recursion",
      "queue", "segment-tree", "binary-search-tree", "memoization", "geometry",
      "binary-indexed-tree", "hash-function", "combinatorics", "topological-sort", "string-matching",
      "shortest-path", "rolling-hash", "Game Theory", "Interactive", "Data Stream",
      "Brainteaser", "Monotonic Queue", "Randomized", "Merge Sort", "Iterator",
      "Concurrency", "Doubly-Linked List", "Probability and Statistics", "Quickselect", "Bucket Sort",
      "Suffix Array", "Minimum Spanning Tree", "Counting Sort", "Shell", "Line Sweep",
      "Reservoir Sampling", "Strongly Connected Component", "Eulerian Circuit", "Radix Sort", "Rejection Sampling",
      "Biconnected Component"
    ]
    RE = r'\[\s*(\d+)\]'

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
  parser.add_argument('--extract', default=False, type=bool)
  parser.add_argument('--level', type=str)
  
  parser.add_argument('--insert', type=str, choices=['data', 'solution'])
  parser.add_argument('--path', required=True, type=str)
  parser.add_argument('--volume', required=True, type=int)
  args = parser.parse_args()

  leetcode = Leetcode()
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
    insert_problem_info(args.path, args.volume)
  if args.insert == 'solution':
    insert_problem_solution(args.path, args.volume)

# $ python3.10 lib/leetcode.py --insert data --path ./data/leetcode/{e, m, h}
# $ python3.10 lib/leetcode.py --insert solution --path ./data/leetcode/solution/{e, m, h}