from dataclasses import dataclass


@dataclass
class Canteen:
    id: int
    name: str
    description: str
    place: str
    photo: list[str]


@dataclass
class DishInfo:
    id: int
    canteen_id: int
    name: str
    category: str
    price: float


@dataclass()
class ResponseModel:
    status_code: int
    data: dict
