from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import SubCategory
from mysite.database.schema import SubCategoryInputSchema, SubCategoryOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

subcategory_router = APIRouter(prefix='/subcategory', tags=['SubCategory CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@subcategory_router.post('/', response_model=SubCategoryOutSchema)
async def create_subcategory(subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    subcategory_db = SubCategory(**subcategory.dict())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db

@subcategory_router.get('/', response_model=List[SubCategoryOutSchema])
async def list_subcategory(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()

@subcategory_router.get('/{subcategory_id}', response_model=SubCategoryOutSchema)
async def detail_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).one_or_none()
    if not subcategory_db:
        raise HTTPException(detail='Subcategory not found', status_code=404)
    return subcategory_db

@subcategory_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: SubCategoryInputSchema,
                          db: Session = Depends(get_db) ):
   category_db =  db.query(SubCategory).filter(SubCategory.id==category_id).first()
   if not category_db:
       raise HTTPException(status_code=404, detail='Category not found')

   for category_key, category_value in category.dict().items():
       setattr(category_db, category_key, category_value)

   db.commit()
   db.refresh(category_db)
   return {'message': 'Category change'}



@subcategory_router.delete('/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(SubCategory).filter(SubCategory.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'Category was delete'}