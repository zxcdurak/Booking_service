from datetime import date
from fastapi import APIRouter
from app.hotels.schemas import SLeftHotels, Shotels
from app.hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("")
async def get_hotels() -> list[Shotels]:
    return await HotelService.find_all()

@router.get("/{location}")
async def get_left_hotels(location: str, date_from:date, date_to:date):
    return await HotelService.get_left_hotels(location, date_from, date_to)

@router.get("/id/{id}", response_model=Shotels)
async def get_hotel(id: int):
    return await HotelService.find_by_id(id)