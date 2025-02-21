

from datetime import datetime
from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import IncorrectTokenFormatException, TokenAbscentException, TokenExpireException, UserIsNotPresentException
from app.users.service import UserService

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbscentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (expire < datetime.now().timestamp()):
        raise TokenExpireException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    return user
    
