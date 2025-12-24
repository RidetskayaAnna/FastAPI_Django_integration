from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from .models import Base, Product
from .database import engine, SessionLocal
from .schemas import ProductCreate, Product as DbProduct, Price

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products", response_model=DbProduct)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, description=product.description, price=product.price, is_available=product.is_available)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@app.get("/products/{product_id}", response_model=DbProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=DbProduct)
def put_product(product_id: int, product_update: ProductCreate,  db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = product_update.name
    product.description = product_update.description
    product.price = product_update.price
    product.is_available = product_update.is_available
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product with id {product_id} has been deleted"}

#for Django
@app.get("/products", response_model=List[DbProduct])
@app.get("/api/v1/products/all", response_model=List[DbProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/api/v1/products/prices", response_model=List[Price])
def get_price(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": p.id, "price": p.price} for p in products]