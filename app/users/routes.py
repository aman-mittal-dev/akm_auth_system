from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users")

@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return {"user": user}

@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"msg": "Welcome Admin"}