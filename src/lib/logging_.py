import os, json, time

def to_file(directory, file_name, data, data_type=None):
  current_time = time.localtime()
  formatted_time = time.strftime('%Y%m%d-%H%M%S', current_time)
  path = f'{directory}'
  # base, extension = os.path.splitext(f'{directory}/{file_name}')
  if not os.path.exists(directory):
      os.makedirs(directory)
  while os.path.exists(f'{directory}'):
      path = f'{directory}_{formatted_time}'
      os.makedirs(path)
  if data_type == 'json':
    with open(f'{path}/{file_name}', "w", encoding='utf-8') as json_file:
      json.dump(data, json_file, ensure_ascii=False)
  else:
    with open(f'{path}/{file_name}', 'w') as f:
      f.write(data)
