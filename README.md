# CoVL: Code + VectorDB + LLM
CoVL is prototype source code before implementing RAG for testing usecases of vector database. 

The development environments are as follows:
- Vector database: Milvus
- Source Data: LeetCode, Grepp
- LLM: gpt, own-model(planning)
- Framework: LlamaIndex (planning)

### pre-required: Docker(mandatory), venv(optional)
You need to install Docker to start Milvus server.

Or you can use [Milvus Lite](https://milvus.io/docs/milvus_lite.md) without Docker.
But CoVL might not well work with Milvus Lite.

### 1. Start milvus standalone server (local)
`docker-compose -f ../docker/docker-compose.yml up -d`

### + Check Milvus with Attu
Access `localhost:8000` and connect to `milvus-standalone` database.

You can use GUI for Milvus with [Attu](https://github.com/zilliztech/attu).

### 2. Modify config
Go to ./src/lib/config.py and Set the configuration.
1. OpenAI API:

OpenAI API is for 2 purposes.

- For Vector embedding model: 'text-embedding-3-small'
- For LLM model: 'gpt-3.5-turbo'

You can change model at config.py

2. Milvus config

This code uses `HNSW` algorithm and `L2` metric for indexing.
For query, `L2` metric is used.

If you need, you can change index-type or metric-type.

You can see [Index list](https://milvus.io/docs/index.md#floating) and [Metric list](https://milvus.io/docs/metric.md) supported by Milvus.

### 3. Data Ingestion and Milvus
At `./src/main.py`, CoVL ingests data, Leetcode and Grepp, to vector database.

Command are different depending on data because The data is managed in different schemas in their respective collections.

#### Command for leetcode 
1. Ingestion data by the problem number

    `python main.py --service 'leetcode' --number 1385 279 70 121`
    
    Problem [1385], [279], [70], [121] will be inserted to Milvus.

2. Ingestion data by level and amount of problem

    `python main.py --service 'leetcode' --level 'h' --volume 5`

    Five problems of Hard level will be inserted to Milvus.

    If you give level 'all',

    `python main.py --service 'leetcode' --level 'all' --volume 5`

    Five problems each level(hard, medium, easy) will be inserted to Milvus. (total 15 problems)

3. Choose code language (If you need, default is python3).

Add `--languague` command (but, **`python3` recommended**).

`python main.py --service 'leetcode' --number 1385 279 70 121 --language 'python3'`

`python main.py --service 'leetcode' --level 'all' --volume 5 --language 'java'`

#### Command for Grepp
Grepp mode only support command by level&volume.

### 4. Query
At `./src/qa.py`, CoVL queries the top 5 most similar problems.

When you specify a leetcode or grepp problem number, it embeds the description of that problem and computes its similarity to the embedding field in the vector db. Then, it returns the five most similar.

#### Example:

`python qa.py --service 'leetcode' --query 49`

Embed the description of leetcode problem #49 (whether or not it's in vector db) and return the 5 most similar problems to the embedding field in vector db.

**CoVL yet supports grepp query. (Implementing)**

