import os, json, time

def to_file(path, data, type=None):
  current_time = time.localtime()
  formatted_time = time.strftime('%Y%m%d-%H%M%S', current_time)
  base, extension = os.path.splitext(path)
  while os.path.exists(path):
      path = f'{base}_{formatted_time}{extension}'
  if type == 'json':
    with open(f"{path}-{formatted_time}", "w") as json_file:
      json.dump(data, json_file)
  else:
    with open(path, 'w') as f:
      f.write(data)
