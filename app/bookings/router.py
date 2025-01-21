from datetime import date
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.exceptions import BookingCannotBeDeleted, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingService.find_all(user_id=user.id)


@router.post("/add")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    new_booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not new_booking:
        raise RoomCannotBeBooked
    else:
        booking_dict = parse_obj_as(SBooking, new_booking).dict()
        send_booking_confirmation_email.delay(booking_dict, user.email)
        return booking_dict
    
@router.delete("/delete", status_code=204)
async def delete_booking(booking_id:int, user: Users = Depends(get_current_user)):
    delete_element = await BookingService.delete(id=booking_id, user_id=user.id)
    if not delete_element:
        raise BookingCannotBeDeleted