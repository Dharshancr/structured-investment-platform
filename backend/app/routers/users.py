from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserRead
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

