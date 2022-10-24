from fastapi import APIRouter
from logistics.models.orders import ReceivedOrderModel
from logistics.scheduler import schedule

orders_router = APIRouter(prefix='/orders')


@orders_router.post('/create')
async def create(order: ReceivedOrderModel):
    is_successfully = await schedule(order)
    return {'successfully': is_successfully}
