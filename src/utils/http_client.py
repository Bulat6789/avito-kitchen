import httpx
from src.config import settings
from src.schemas import OrderStatus

async def notify_restaurant(order_id: int, restaurant_id: int, status: OrderStatus):
    """Уведомляет ресторан о новом заказе"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "order_id": order_id,
                "restaurant_id": restaurant_id,
                "status": status.value
            }
            # Эндпоинт, который ожидает сервис-ресторан
            url = f"{settings.RESTAURANT_API_URL}/webhook/new_order"
            await client.post(url, json=payload, timeout=5.0)
    except Exception as e:
        # В реальном проекте тут бы логгирование, в рамках MVP — просто печатаем
        print(f"Failed to notify restaurant: {e}")