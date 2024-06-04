import subprocess, time, re
from tqdm import tqdm
from lib.logging_ import to_file

FILE_PATH = "./data/leetcode/leetcode.json"
SOURCE_PATH = './data/leetcode/leetcode-source-file'

class Leetcode:
  def __init__(self) -> None:
    pass

  def get_problem(self, index, language):
    array = [
        [], # 0 pNumber
        [], # 1 title
        [], # 2 level
        [], # 3 description
        [], # 4 example 
        [], # 5 constraint
        [], # 6 output
    ]
    for i in tqdm(index):
      array[0].append(i)
      raw = subprocess.run(
          f"leetcode show {i} -g -x -o {SOURCE_PATH} -l {language}", 
          shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
      ).stdout.decode("utf-8")
      document = raw.split('\n')
      
      array[1].append(document[0])

      if 'Easy' in document[9]:
        array[2].append('e')
      if 'Medium' in document[9]:
        array[2].append('m')
      if 'Hard' in document[9]:
        array[2].append('h')
      
      desc = ''
      desc_index = [i for i in range(len(document)) if '* Testcase Example:  ' in document[i]]
      for line in range(desc_index[0]+1, len(document)):
        desc += document[line]
      array[3].append(desc)

      example = ''
      constraint = ''
      example_index = [i for i in range(len(document)) if 'Example' in document[i]]
      constraint_index = [i for i in range(len(document)) if 'Constraints:' in document[i]]

      for line in range(example_index[0], constraint_index[0]-1):
        example += document[line]
      array[4].append(example)

      for line in range(constraint_index[0], len(document)):
        constraint += document[line]
      array[5].append(constraint)

      output=''
      output_code_index = [line for line in range(len(document)) if '* Source Code:       ' in document[line]]
      source_file = document[output_code_index[0]]
      code_name = source_file[source_file.find(str(i)):source_file.find('.py')+3]

      with open (f'{SOURCE_PATH}/{code_name}', "r") as f:
          lines = f.readlines()
          for line in lines:
              if '#' not in line:
                  output += line
              else:
                  continue
      array[6].append(output)
      to_file(FILE_PATH, array, 'json')

    return array

  def get_problems_with_level(self, language, level, volume):
    if level == 'all':
      problem_list = []
      for l in ['h', 'm', 'e']:
        print(f'========== Level: {l} ==========')
        result = subprocess.run(f"leetcode list -q {l}L -s", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
        time.sleep(10)
        raw = result.split("\n")
        problem_number = re.compile('\[([^]]+)\]')
        for i in tqdm(range(volume)):
          problem_list.append(int(problem_number.findall(raw[i])[0]))
      data = self.get_problem(problem_list, language)
      return data
    else:
      result = subprocess.run(f"leetcode list -q {level}L -s", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
      time.sleep(10)
      raw = result.split("\n")
      problem_list = []
      problem_number = re.compile('\[([^]]+)\]')
      for i in range(volume):
        problem_list.append(int(problem_number.findall(raw[i])[0]))
      data = self.get_problem(problem_list, language)
      return data




