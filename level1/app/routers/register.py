
from fastapi import Depends, status, APIRouter,HTTPException
from app import schemas,models,utils
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router=APIRouter(prefix="/register", tags=['Register'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.RegisterUserOut)
def register_user(dets:schemas.RegisterUser, db:Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email == dets.email).first()
    if user:
        raise HTTPException(status_code=403, detail="User with mail id already exists")
    hashed_password= utils.hash(dets.password)
    dets.password= hashed_password
    new_user=models.User(**dets.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




