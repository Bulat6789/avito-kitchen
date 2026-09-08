from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.routes import restaurants, menu, orders, webhook

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Авито.Кухня API",
    description="MVP для заказа еды из ресторанов",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(webhook.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "avito-kitchen-api"}