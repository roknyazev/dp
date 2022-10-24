from logistics.models.orders import ReceivedOrderModel, ScheduledOrderModel
import logistics.context as context


async def schedule(received_order: ReceivedOrderModel) -> bool:
    received_order_id = context.order_count
    context.order_count += 1
    path = await calc_path(received_order.node1, received_order.node2)
    scheduled_order = ScheduledOrderModel(id=received_order_id, path=path)
    context.scheduled_orders.append(scheduled_order)
    return True
