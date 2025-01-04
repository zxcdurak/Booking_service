from app.hotels.rooms.schemas import SRooms
from app.hotels.router import router
from app.hotels.rooms.service import RoomService

@router.get("/{hotel_id}/rooms", response_model=list[SRooms])
async def get_rooms(hotel_id:int):
    return await RoomService.find_all(hotel_id=hotel_id)