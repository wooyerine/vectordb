from pymilvus import FieldSchema, DataType
from lib.config import Milvus

leetcode_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='problem_id', dtype=DataType.INT64),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='testcases', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='source_code_name', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='code_template', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='desc_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

grepp_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='problem_id', dtype=DataType.INT64),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='partTitle', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='level', dtype=DataType.INT64),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='testCases', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='desc_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

leetcode_v2_fields = [
#   FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='problem_id', dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='topic', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='testcases', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='code_template', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

integrate_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='type', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='problem_id', dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='topic', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='languages', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=900, max_length=1000),
    FieldSchema(name='level', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='examples', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='constraints', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='testcases', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='code_template', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

grepp_solution_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='challenge_id', dtype=DataType.INT64),
    FieldSchema(name='solution_id', dtype=DataType.INT64),
    FieldSchema(name='code', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='code_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

leetcode_solution_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='problem_id', dtype=DataType.INT64),
    FieldSchema(name='solution_id', dtype=DataType.INT64),
    FieldSchema(name='code', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='code_embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

robotics_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]

robotics_overlapped_fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=64000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=Milvus['DIMENSION']),
]
