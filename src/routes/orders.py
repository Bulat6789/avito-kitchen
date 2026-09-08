from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from src import crud, schemas
from src.database import get_db
from src.utils.http_client import notify_restaurant

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        db_order = crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # В фоне уведомляем ресторан о новом заказе
    background_tasks.add_task(
        notify_restaurant,
        db_order.id,
        db_order.restaurant_id,
        schemas.OrderStatus.PENDING
    )

    return db_order

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/restaurant/{restaurant_id}", response_model=List[schemas.OrderResponse])
def get_orders_by_restaurant(restaurant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders_by_restaurant(db, restaurant_id, skip=skip, limit=limit)

@router.patch("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order_status(db, order_id, status_update.status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order