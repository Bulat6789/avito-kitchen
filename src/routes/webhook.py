from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, schemas
from src.database import get_db

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("/restaurant")
def restaurant_webhook(payload: schemas.WebhookPayload, db: Session = Depends(get_db)):
    """
    Эндпоинт для ресторанов, чтобы они обновляли статус заказа.
    """
    order = crud.update_order_status(db, payload.order_id, payload.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": "ok", "order_id": payload.order_id}