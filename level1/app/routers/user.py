from app import schemas,models,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter,HTTPException,Query
from typing import Optional

router=APIRouter(prefix="/user")


@router.get("/get")
def get_all_users( db:Session= Depends(get_db)):
    users=db.query(models.User).all()
    print(users)
    return users


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.RegisterUserOut)
def get_user_by_id(user_id: int, current_user= Depends(oauth2.get_current_user),db:Session= Depends(get_db)):
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

@router.delete("/delete/{admin_id}", status_code=status.HTTP_200_OK)
def delete_user(admin_id: int, user:schemas.DeleteUser, current_admin= Depends(oauth2.get_current_admin), db:Session = Depends(get_db)):
    if  current_admin.id != admin_id:
        raise HTTPException(status_code=404, detail="invalid")

    users=db.query(models.User).filter(models.User.id == user.user_id).first()
    db.delete(users)
    db.commit()
   
    return {"message": "user deleted"}

#FILTERING,PAGINATION,SEARCH


@router.get("/filter", status_code=status.HTTP_200_OK)
def get_users(
    name: Optional[str] = Query(None, description="Search by name"),
    email: Optional[str] = Query(None, description="Search by email"),
    sort_by: Optional[str] = Query(
        None,
        enum=["age", "created_at"],
        description="Field to sort by"
    ),
    order: str = Query(
        "asc",
        enum=["asc", "desc"],
        description="Sort order"
    ),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.User)

    # 🔍 Filtering
    if name:
        query = query.filter(models.User.name.ilike(f"%{name}%"))

    if email:
        query = query.filter(models.User.email.ilike(f"%{email}%"))

    # 🔃 Sorting with direction
    if sort_by:
        column = getattr(models.User, sort_by)

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    # 📄 Pagination
    users = query.offset(offset).limit(limit).all()

    return users