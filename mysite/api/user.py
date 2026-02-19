from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema,UserProfileOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix='/user', tags=['User CRUD'])#путь crud функсия бар
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())#jsonго келген маалыматтарды
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db:Session = Depends(get_db)):
    return  db.query(UserProfile).all()



@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
async def detail_user(user_id:int, db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок',status_code=400,)
    return user_db




@user_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: UserProfileInputSchema,
                          db: Session = Depends(get_db) ):
   category_db =  db.query(UserProfile).filter(UserProfile.id==category_id).first()
   if not category_db:
       raise HTTPException(status_code=404, detail='Category not found')

   for category_key, category_value in category.dict().items():
       setattr(category_db, category_key, category_value)

   db.commit()
   db.refresh(category_db)
   return {'message': 'Category change'}



@user_router.delete('/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(UserProfile).filter(UserProfile.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category_db)
    db.commit()
    return {'message': 'Category was delete'}


