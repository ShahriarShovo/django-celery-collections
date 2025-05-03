import hashlib
import uuid

def generate_token():
    return str(uuid.uuid4())

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token_hash(raw_token, stored_hash):
    return hash_token(raw_token) == stored_hash
