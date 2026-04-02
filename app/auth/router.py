from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth.hashing import hash_password, verify_password, validate
from app.auth.jwt_handler import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(res: Response, user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"data": None, "message": "User already exists", "status": status.HTTP_400_BAD_REQUEST}
    
    # Validate password
    validation_password = validate(user.password)
    if validation_password is not None:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"data": None, "message": validation_password, "status": status.HTTP_400_BAD_REQUEST}
    
    db_user = User(email=user.email, password=hash_password(user.password))

    db.add(db_user)
    db.commit()
    res.status_code = status.HTTP_201_CREATED
    return {"data": db_user, "message": "User created", "status": status.HTTP_201_CREATED}


@router.post("/login")
def login(res: Response, user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"data": None, "message": "User not found", "status": status.HTTP_400_BAD_REQUEST}

    if not verify_password(user.password, db_user.password):
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {"data": None, "message": "Incorrect password", "status": status.HTTP_400_BAD_REQUEST}

    access = create_access_token({"user_id": db_user.id, "role": db_user.role})
    refresh = create_refresh_token({"user_id": db_user.id})

    res.status_code = status.HTTP_200_OK
    return {"data": {"access_token": access, "refresh_token": refresh}, "message": "Login successful", "status": status.HTTP_200_OK}