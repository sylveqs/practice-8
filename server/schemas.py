from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock_quantity: int = 0
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True