from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Product
from mysite.database.schema import ProductInputSchema, ProductOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_router = APIRouter(prefix='/product',  tags=['Product CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductOutSchema)
async def create_product(
    product: ProductInputSchema,
    db: Session = Depends(get_db)
):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/', response_model=List[ProductOutSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.get('/{product_id}', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).one_or_none()
    if not product_db:
        raise HTTPException(detail='Product not found', status_code=404)
    return product_db


@product_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: ProductInputSchema,
                          db: Session = Depends(get_db) ):
   category_db =  db.query(Product).filter(Product.id==category_id).first()
   if not category_db:
       raise HTTPException(status_code=404, detail='Category not found')

   for category_key, category_value in category.dict().items():
       setattr(category_db, category_key, category_value)

   db.commit()
   db.refresh(category_db)
   return {'message': 'Category change'}



@product_router.delete('/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Product).filter(Product.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'Category was delete'}