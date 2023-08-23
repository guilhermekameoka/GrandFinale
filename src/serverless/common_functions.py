import json
import boto3
import urllib3
import hashlib
from io import BytesIO


def unique_str_id(string: str, last_idx: int = 12) -> str:

    m = hashlib.md5()
    string = string.encode('utf-8')
    m.update(string)
    unique_name: str = str(int(m.hexdigest(), 16))[0:last_idx]

    return unique_name
    

    
