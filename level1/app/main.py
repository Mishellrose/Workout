from fastapi import FastAPI
from . import models
from app.database import engine
from app.logger import logger
from app.routers import user,register,auth


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(register.router)
app.include_router(auth.router)
app.include_router(user.router)



@app.on_event("startup")
def startup_event():
    logger.info("Application started")

