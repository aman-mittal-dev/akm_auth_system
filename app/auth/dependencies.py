from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(res: Response, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return payload
    except:
        res.status_code = status.HTTP_401_UNAUTHORIZED
        return {"data": None, "messge": "Invalid Token", "status": status.HTTP_401_UNAUTHORIZED}


def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != role:
            return {"data": None, "message": "Forbidden", "status": status.HTTP_403_FORBIDDEN}
        return user
    return role_checker