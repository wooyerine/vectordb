## OpenAI + Huggling-Face-datasets + Milvus + Attu
Just text querying from Vector Database Milvus with openAI embedding model and Huggling-face datasets(netflix movies).
Attu is a GUI for Milvus.
Reference: https://cookbook.openai.com/examples/vector_databases/milvus/filtered_search_with_milvus_and_openai

### pre-required: Docker(mandatory), venv(optional)
for virtual environment => `python -m venv .venv`

### 1. pip install
`pip install -r requirements.txt`

Notice: Open AI embedding does not support any more, so you need to install to version `openai==0.28`.

### 2. Start milvus server (local)
`docker-compose -f ../../docker/docker-compose.yml up -d`

### 3. Modify config
change Open AI API_KEY.
If you need, you can change index-type or metric-type.
You can see [Index list](https://milvus.io/docs/index.md#floating) and [Metric list](https://milvus.io/docs/metric.md) supported by Milvus.

### 4. Query
`python main.py`

### + Check Milvus with Attu
Access `localhost:8000` and connect to `milvus-standalone` database.
You can use GUI for Milvus with [Attu](https://github.com/zilliztech/attu).
