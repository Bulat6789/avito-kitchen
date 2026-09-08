import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum

app = FastAPI(title="Example Restaurant Service", version="1.0.0")

MAIN_API_URL = os.getenv("MAIN_API_URL", "http://main-api:8000")


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class NewOrderPayload(BaseModel):
    order_id: int
    restaurant_id: int
    status: OrderStatus


class StatusUpdatePayload(BaseModel):
    order_id: int
    new_status: OrderStatus


@app.post("/webhook/new_order")
async def receive_new_order(payload: NewOrderPayload):
    """
    Ресторан получает уведомление о новом заказе.
    В продакшне здесь бы логика: принят/отклонён, отправка на кухню и т.д.
    """
    print(f"📦 Новый заказ #{payload.order_id} для ресторана {payload.restaurant_id}")

    # В демо-режиме автоматически принимаем заказ через 2 секунды (имитация)
    # Для упрощения используем синхронный код с asyncio.create_task
    import asyncio
    asyncio.create_task(auto_accept_order(payload.order_id))

    return {"status": "received"}


async def auto_accept_order(order_id: int):
    import asyncio
    await asyncio.sleep(2)

    # Сначала принимаем
    await update_order_status(order_id, OrderStatus.ACCEPTED)
    await asyncio.sleep(3)
    # Потом начинаем готовить
    await update_order_status(order_id, OrderStatus.PREPARING)
    await asyncio.sleep(5)
    # Заказ готов
    await update_order_status(order_id, OrderStatus.READY)


async def update_order_status(order_id: int, status: OrderStatus):
    """Вызывает API основного сервиса, чтобы обновить статус"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{MAIN_API_URL}/orders/{order_id}/status"
            payload = {"status": status.value}
            response = await client.patch(url, json=payload, timeout=5.0)
            if response.status_code != 200:
                print(f"⚠️ Ошибка обновления статуса: {response.status_code}")
            else:
                print(f"✅ Статус заказа #{order_id} обновлён на {status.value}")
    except Exception as e:
        print(f"❌ Не удалось обновить статус: {e}")


@app.get("/health")
def health():
    return {"status": "ok", "service": "restaurant-example"}


@app.get("/debug/orders")
async def debug_orders():
    """Для отладки — получить все заказы ресторана через основной API"""
    try:
        async with httpx.AsyncClient() as client:
            # В реальности у ресторана есть свой restaurant_id, здесь для примера 1
            response = await client.get(f"{MAIN_API_URL}/orders/restaurant/1")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))