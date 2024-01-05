import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys
# Load environment variables from .env file
sys.path.append("..") # added!
load_dotenv()

def generate_jwt_token(payload,lifetime=120):
        # Generates a new JWT token, wrapping information provided by payload (dict)
    # Lifetime describes (in minutes) how much time the token will be valid
    if lifetime:
        payload["exp"] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()

    return jwt.encode(payload, os.environ.get('SECRET_KEY', algorithm="HS256"))

def decote_jwt_token(token):
    return jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])