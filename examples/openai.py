# Similarity Search with Milvus and OpenAI

import csv
import json
import random
import time
from openai import OpenAI
# pip install pymilvus
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

