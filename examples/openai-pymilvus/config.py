# Milvus Config
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
    "OPENAI_ENGINE" : 'text-embedding-3-small',
    "API_KEY" : sk-***,
    "BATCH_SIZE" : 10
}

Data =\
{
    "netflix-shows": 'hugginglearners/netflix-shows'
}
