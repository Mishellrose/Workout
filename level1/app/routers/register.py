
from fastapi import Depends, status, APIRouter,HTTPException
from app import schemas,models,utils,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router=APIRouter(prefix="/register", tags=['Register'])



@router.post("/admin", status_code=status.HTTP_201_CREATED,response_model= schemas.AdminOut)
def create_admin(dets: schemas.AdminCreate, db:Session= Depends(get_db)):
    admin= db.query(models.Admin).filter(models.Admin.email == dets.email).first()
    if admin: 
        raise HTTPException(status_code=403, detail="Admin with mail id already exists")
    hashed_password= utils.hash(dets.password)
    dets.password= hashed_password
    new_admin=models.Admin(**dets.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin



@router.post("/user/{admin_id}", status_code=status.HTTP_201_CREATED, response_model= schemas.RegisterUserOut)
def create_user(admin_id: int, dets:schemas.RegisterUser, current_admin=Depends(oauth2.get_current_admin), db:Session = Depends(get_db)):
    if current_admin.id != admin_id:
        raise HTTPException(status_code=403, detail="Invalid")
    print(admin_id)
    print(current_admin)
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


