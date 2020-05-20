import hashlib 
import json 

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

