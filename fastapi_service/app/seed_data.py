from sqlalchemy.orm import Session
from .models import Base, Product
from .database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    if db.query(Product).count() == 0:
        test_products = [
            {"name": "Laptop", "description": "Gaming laptop", "price": 1500.0, "is_available": True},
            {"name": "Smartphone", "description": "Latest smartphone", "price": 800.0, "is_available": True},
            {"name": "Headphones", "description": "Wireless headphones", "price": 200.0, "is_available": True},
            {"name": "Mouse", "description": "Gaming mouse", "price": 100.0, "is_available": False},
            {"name": "Keyboard", "description": "Mechanical keyboard", "price": 150.0, "is_available": True},
            {"name": "Monitor", "description": "27-inch monitor", "price": 300.0, "is_available": True},
            {"name": "Tablet", "description": "Graphics tablet", "price": 500.0, "is_available": False},
            {"name": "Flash drive", "description": "128GB USB flash drive", "price": 50.0, "is_available": True},
            {"name": "Webcam", "description": "4K web camera", "price": 120.0, "is_available": True},
            {"name": "Speakers", "description": "Stereo speakers", "price": 80.0, "is_available": True},
            {"name": "Router", "description": "Wi-Fi 6 router", "price": 180.0, "is_available": True},
        ]
        for data in test_products:
            product = Product(**data)
            db.add(product)
        db.commit()
    else:
        print("Data exists")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()