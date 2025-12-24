from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class Price(BaseModel):
    id: int
    price: float