from app import schemas,models
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter,HTTPException


router=APIRouter(prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(dets:schemas.UserCreate, db:Session=Depends(get_db)):
    if dets.age<0 :
        raise HTTPException(status_code=403, detail="Invalid age")
    user=db.query(models.User).filter(models.User.email == dets.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User with same email id exists, create new user with a different email")
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
    if not user:
        raise HTTPException(status_code=404, detail="No user with the id")
    print(user)
    return user

@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user_update: schemas.UpdateUser,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:int, db:Session = Depends(get_db)):
    users=db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
   
    return {"message": "user deleted"}