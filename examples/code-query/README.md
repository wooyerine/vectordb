# Pre-Required
1. `npm` for leetcode-cli install

# Dependencies
1. leetcode-cli:
  1. install with npm: `npm install -g leetcode-cli`
  2. version check: `leetcode version`
  3. session login: `leetcode user -l`
2. Milvus container start: `cd ... && docker-compose -f ./docker/docker-compose.yml up -d`

# Start
`cd examples/code-query && python3 main.py`
1. Extract Data from leetcode (`./data/data.py`)
2. Create and connect to milvus collection (`./milvus.py`)
3. Insert data (`./milvus.py`)
순으로 진행

# Attu GUI
Access `localhost:8000` and connect to `milvus-standalone` database.
You can use GUI for Milvus with [Attu](https://github.com/zilliztech/attu).
