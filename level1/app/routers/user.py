from app import schemas,models
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter

router=APIRouter(prefix="/user")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(dets:schemas.UserCreate, db:Session=Depends(get_db)):
    new_user=models.User(**dets.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  

@router.get("/get")
def get_all_users(db:Session= Depends(get_db)):
    users=db.query(models.User).all()
    print(users)
    return users


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db:Session= Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    return user