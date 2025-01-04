from pydantic import BaseModel

class Shotels(BaseModel):
    id: int
    name: str
    location: str
    services: list
    image_id: int
    rooms_quantity: int

class SLeftHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list
    image_id: int
    rooms_quantity: int
    rooms_left: int