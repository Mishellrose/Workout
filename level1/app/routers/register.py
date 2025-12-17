
from fastapi import Depends, status, APIRouter,HTTPException
from app import schemas,models,utils,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.logger import logger




router=APIRouter(prefix="/register", tags=['Register'])



@router.post("/admin", status_code=status.HTTP_201_CREATED,response_model= schemas.AdminOut)
def create_admin(dets: schemas.AdminCreate, db:Session= Depends(get_db)):
    logger.info(f"creating admin with email={dets.email}")
    admin= db.query(models.Admin).filter(models.Admin.email == dets.email).first()
    if admin: 
        logger.warning("admin creation failed :email already exists")
        raise HTTPException(status_code=403, detail="Admin with mail id already exists")
    hashed_password= utils.hash(dets.password)
    dets.password= hashed_password
    new_admin=models.Admin(**dets.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    logger.info(f"Admin created successfully id={new_admin.id}")
    return new_admin



@router.post("/user/{admin_id}", status_code=status.HTTP_201_CREATED, response_model= schemas.RegisterUserOut)
def create_user(admin_id: int, dets:schemas.RegisterUser, current_admin=Depends(oauth2.get_current_admin), db:Session = Depends(get_db)):
    logger.info(f"Creating user with email={dets.email}")
    if current_admin.id != admin_id:
        logger.warning("User creation failed")
        raise HTTPException(status_code=403, detail="Invalid")
   
    user=db.query(models.User).filter(models.User.email == dets.email).first()
    if user:
        raise HTTPException(status_code=403, detail="User with mail id already exists")
    hashed_password= utils.hash(dets.password)
    dets.password= hashed_password
    new_user=models.User(**dets.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created successfully id={new_user.id}")
    return new_user


