import os, json, time

def to_file(directory, file_name, data, data_type=None):
  if not os.path.exists(directory):
      os.makedirs(directory)
  
  if data_type == 'json':
    with open(f'{directory}/{file_name}', "w", encoding='utf-8') as json_file:
      json.dump(data, json_file, ensure_ascii=False)
  else:
    with open(f'{directory}/{file_name}', 'w') as f:
      f.write(data)

# JSON 데이터를 50개씩 쪼개서 저장하는 함수
def save_json_in_chunks(data, chunk_size=100, base_filename='./data/leetcode'):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        filename = f"{base_filename}/{i//chunk_size + 1}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=4)
