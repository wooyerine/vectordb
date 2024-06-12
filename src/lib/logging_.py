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
