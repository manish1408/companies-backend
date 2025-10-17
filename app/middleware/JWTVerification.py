from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from typing import Dict, Any

def jwt_validator(
    auth: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Dict[str, Any]:
    secret_key: str = os.getenv("JWT_SECRET")
    algorithm: str = "HS256"  # Changed from RS256 to HS256 for consistency
    token = auth.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload

    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid or expired token.")