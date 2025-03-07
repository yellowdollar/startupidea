from fastapi import FastAPI
from api.users import user_router

from database.database import init_models

app = FastAPI()
app.include_router(router = user_router)

@app.on_event('startup')
async def startup():
    await init_models()