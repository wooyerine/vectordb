# Configuration

Milvus =\
{
    "HOST" : '127.0.0.1',
    "PORT" : 19530,
    "DIMENSION" : 1536,
    "INDEX_PARAM" : {
        'metric_type':'L2',
        'index_type':"HNSW",
        'params':{'M': 8, 'efConstruction': 64}
    },
    "QUERY_PARAM" : {
        "metric_type": "L2",
        "params": {"ef": 64},
    }
}

Openai =\
{
    "EMBED_MODEL" : 'text-embedding-3-small',
    "LLM_MODEL" : 'gpt-3.5-turbo',
    "API_KEY" : 'sk-***',
    "BATCH_SIZE" : 10
}

Account =\
{
    "EMAIL" : 'etri-test@grepp.co',
    "PW" : ''
}
