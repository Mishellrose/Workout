from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,utils,oauth2
from app.database import get_db


router=APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_credens:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email == user_credens.username).first()
    if not user:
        raise HTTPException(status=403, detail="no user")
    if not utils.verify(user_credens.password, user.password):
        raise HTTPException(status=404, detail="wrong credentials")
    access_token=oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    