import hashlib
import re
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

ACCESS_TOKEN_EXPIRE_MINUTES = 1440
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate(password):
    special_characters = r"[!@#$%^&*()]"

    if not (len(password) >= 6 and len(password) <= 25):
        return "Password must be between 6 and 25 characters long"
    if not re.search(r"[A-Z]", password):
        return "Password must include at least one uppercase letter(A-Z)"
    if not re.search(r"[a-z]", password):
        return "Password must include at least one lowercase letter(a-z)"
    if not re.search(r"\d", password):
        return "Password must include at least one digit (0-9)"
    if not re.search(special_characters,password):
        return "Password must include at least one special character: !@#$%^&*()"
    return None

def preprocess_password(password: str) -> str:
    # Convert to SHA256 first (fixed length)
    return hashlib.sha256(password.encode()).hexdigest()

def hash_password(password: str):
    password = preprocess_password(password)
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    password = preprocess_password(password)
    return pwd_context.verify(password, hashed)
