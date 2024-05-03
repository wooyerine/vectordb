## OpenAI + Huggling-Face-datasets + Milvus
It does not include IlamaIndex.
Just text querying from Vector Database Milvus with openAI and Huggling-face datasets.
Reference: https://cookbook.openai.com/examples/vector_databases/milvus/filtered_search_with_milvus_and_openai

### pre-required: venv
`python -m venv .venv`

### 1. pip install
`pip install -r requirements.txt`

### 2. Start milvus server
`docker-compose -f ../../docker/docker-compose.yml up -d`

### 3. finding_moive.ipynb