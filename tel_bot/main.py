from fastapi import FastAPI
from tel_bot.api import router


from tel_bot.database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
