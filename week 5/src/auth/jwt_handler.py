import time
import jwt
import os
import json
from typing import Dict

# Load config
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '..', '..', 'config', 'auth_config.json')

# Defaults
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        conf = json.load(f)
        SECRET_KEY = conf.get("secret_key", SECRET_KEY)
        ALGORITHM = conf.get("algorithm", ALGORITHM)
        ACCESS_TOKEN_EXPIRE_MINUTES = conf.get("access_token_expire_minutes", 30)

def create_access_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception:
        return None
