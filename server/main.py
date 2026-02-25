from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
import models
import schemas
import crud

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API", description="API для каталога товаров")

# Настройка CORS для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "E-Commerce API", "version": "1.0"}

@app.get("/products/all", response_model=List[schemas.Product])
async def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить все товары
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/get/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получить товар по ID
    """
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.post("/products/create/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Создать новый товар
    """
    return crud.create_product(db=db, product=product)

@app.get("/categories/all", response_model=List[schemas.Category])
async def get_all_categories(db: Session = Depends(get_db)):
    """
    Получить все категории
    """
    return crud.get_categories(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)