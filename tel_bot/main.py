from fastapi import FastAPI
from tel_bot.carts.router import router as carts_router
from tel_bot.users.router import router as users_router
from tel_bot.ms_api.router import router as ms_api_router


# from tel_bot.regist_primer.router import router as primer

from tel_bot.database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.include_router(primer)

app.include_router(users_router)
app.include_router(carts_router)
app.include_router(ms_api_router)


