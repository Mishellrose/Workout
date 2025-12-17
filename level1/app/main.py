from fastapi import FastAPI
from . import models
from app.database import engine

from app.routers import user,register,auth


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(user.router)
app.include_router(register.router)
app.include_router(auth.router)

