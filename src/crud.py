from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

from src import models, schemas

# ----- RESTAURANTS -----
def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).filter(models.Restaurant.is_active == True).offset(skip).limit(limit).all()

def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# ----- MENU -----
def get_menu_items(db: Session, restaurant_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.MenuItem).filter(
        models.MenuItem.restaurant_id == restaurant_id,
        models.MenuItem.is_available == True
    ).offset(skip).limit(limit).all()

def create_menu_item(db: Session, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ----- ORDERS -----
def create_order(db: Session, order: schemas.OrderCreate):
    # Рассчитываем сумму
    total = 0.0
    order_items = []
    for item in order.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise ValueError(f"Menu item {item.menu_item_id} not found")
        if not menu_item.is_available:
            raise ValueError(f"Menu item {menu_item.name} is not available")
        total += menu_item.price * item.quantity
        order_items.append({
            "menu_item_id": item.menu_item_id,
            "quantity": item.quantity,
            "price_at_order": menu_item.price
        })

    db_order = models.Order(
        restaurant_id=order.restaurant_id,
        user_name=order.user_name,
        user_phone=order.user_phone,
        delivery_address=order.delivery_address,
        total_price=total,
        comment=order.comment
    )
    db.add(db_order)
    db.flush()

    for oi in order_items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            menu_item_id=oi["menu_item_id"],
            quantity=oi["quantity"],
            price_at_order=oi["price_at_order"]
        )
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders_by_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(
        models.Order.restaurant_id == restaurant_id
    ).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, new_status: schemas.OrderStatus):
    order = get_order(db, order_id)
    if not order:
        return None
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order