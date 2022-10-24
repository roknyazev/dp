from pydantic import BaseModel
from .path import BasePath


class ReceivedOrderModel(BaseModel):
    node1: int
    node2: int


class ScheduledOrderModel(BaseModel):
    id: int
    path: BasePath

    class Config:
        arbitrary_types_allowed = True
