from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src import crud, schemas
from src.database import get_db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/", response_model=List[schemas.RestaurantResponse])
def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_restaurants(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.RestaurantResponse)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db, restaurant)

@router.get("/{restaurant_id}", response_model=schemas.RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant