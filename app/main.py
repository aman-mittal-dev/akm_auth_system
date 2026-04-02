from fastapi import FastAPI
from app.database import Base, engine
from app.auth.router import router as auth_router
from app.users.routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}