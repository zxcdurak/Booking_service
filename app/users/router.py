from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.exceptions import UserAlreadyExistsException
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.service import UserService
from app.users.schemas import SUserAuth
from app.users.auth import authenticate_user, create_access_token, get_password_hash



router_user = APIRouter(
    prefix="/user",
    tags=["Auth & Пользователи"]
)

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)

@router_auth.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@router_user.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user