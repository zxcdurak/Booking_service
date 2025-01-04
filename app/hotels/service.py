from datetime import date
from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.hotels.models import Hotels
from app.database import async_session_maker, engine

class HotelService(BaseService):
    model = Hotels


    @classmethod
    async def get_left_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            
            booked_rooms = select(Rooms.hotel_id, func.count(Bookings.room_id).label("count")
            ).join(
                Bookings, and_(Rooms.id == Bookings.room_id, or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )),
                isouter=True
            ).group_by(Rooms.hotel_id).subquery()

            
            left_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.image_id,
                Hotels.rooms_quantity,
                (Hotels.rooms_quantity - func.sum(booked_rooms.c.count)).label("rooms_left")
            ).select_from(
                Hotels
            ).join(
                booked_rooms, booked_rooms.c.hotel_id == Hotels.id, isouter=True
            ).filter(
                Hotels.location.like(f'%{location}%')
            ).group_by(
                Hotels.id, booked_rooms.c.count
            ).having(Hotels.rooms_quantity - func.sum(booked_rooms.c.count) > 0)

            #print(left_hotels.compile(engine,compile_kwargs={"literal_binds": True}))
            result = await session.execute(left_hotels)
            return result.mappings().all()