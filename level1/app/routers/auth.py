from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,utils,oauth2
from app.database import get_db
from app.logger import logger

router=APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_credens:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    logger.info(f"Login attempt for user with email={user_credens.username}")
    user=db.query(models.User).filter(models.User.email == user_credens.username).first()
    if not user:
        logger.warning("Login attempt failed:email not found")
        raise HTTPException(status=403, detail="no user")
    if not utils.verify(user_credens.password, user.password):
        logger.warning("Login attempt failed:password incorrect")
        raise HTTPException(status=404, detail="wrong credentials")
    access_token=oauth2.create_access_token(data={"user_id": user.id, "user_type": "user"})
    logger.info(f"Login successful:Access token created for email={user_credens.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/adminlogin", status_code=status.HTTP_200_OK)
def login_admin(admin_credens:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    logger.info(f"Login attempt for admin with email={admin_credens.username}")
    admin=db.query(models.Admin).filter(models.Admin.email == admin_credens.username).first()
    if not admin:
        logger.warning("Login attempt failed:email not found")
        raise HTTPException(status=403, detail="no user")
    if not utils.verify(admin_credens.password, admin.password):
        logger.warning("Login attempt failed:password incorrect")
        raise HTTPException(status=404, detail="wrong credentials")
    access_token=oauth2.create_access_token(data={"user_id": admin.id, "user_type": "admin"})
    logger.info(f"Login successful:Access token created for email={admin_credens.username}")
    return {"access_token": access_token, "token_type": "bearer"}
    