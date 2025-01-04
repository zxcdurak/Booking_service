from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.bookings.models import Bookings
from app.bookings.service import BookingService
from app.hotels.router import get_left_hotels
from app.users.router import read_users_me

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels(request: Request, hotels=Depends(get_left_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={
            "request":request,
            "hotels": hotels                        
            }
        )


@router.get("/my_bookings")
async def get_bookings(request: Request, user=Depends(read_users_me)):
    if not user:
       return RedirectResponse("/authorization")
    bookings = BookingService.find_all(user_id=user.id)
    return templates.TemplateResponse(
        name="bookings.html", context={
            "request":request,
            "bookings": bookings                  
            }
        )