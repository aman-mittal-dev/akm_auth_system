from fastapi import APIRouter, Depends, Response, status
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users")

@router.get("/me")
def get_profile(res: Response, user=Depends(get_current_user)):
    res.status_code = status.HTTP_200_OK
    return {"data": user, "message": "User profile", "status": status.HTTP_200_OK}

@router.get("/admin")
def admin_only(res: Response, user=Depends(require_role("admin"))):
    res.status_code = status.HTTP_200_OK
    return {"data": user, "message": "Welcome Admin", "status": status.HTTP_200_OK}