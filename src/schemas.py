from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

#-----RESTAURANT-----
class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#-----MENU ITEM-----
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    category: Optional[str] = None
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    restaurant_id: int

class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True

#-----ORDER ITEM-----
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_order: float
    menu_item_name: Optional[str] = None

    class Config:
        from_attributes = True

#-----ORDER-----
class OrderCreate(BaseModel):
    restaurant_id: int
    user_name: str
    user_phone: str
    delivery_address: str
    items: List[OrderItemCreate]
    comment: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    restaurant_id: int
    user_name: str
    user_phone: str
    delivery_address: str
    status: OrderStatus
    total_price: float
    comment: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

#-----WEBHOOK-----
class WebhookPayload(BaseModel):
    order_id: int
    status: OrderStatus
    restaurant_id: int