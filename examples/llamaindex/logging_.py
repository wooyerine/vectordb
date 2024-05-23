import os, json

def to_file(path, data, type=None):
  counter = 0
  base, extension = os.path.splitext(path)
  while os.path.exists(path):
      path = f'{base}_{counter}{extension}'
      counter += 1
  if type == 'json':
    with open(f"{path}", "w") as json_file:
      json.dump(data, json_file)
  else:
    with open(path, 'w') as f:
      f.write(data)
