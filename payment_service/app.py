from fastapi import FastAPI
import asyncio
from consumer import consume
from db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()  # ensure table exists
    asyncio.create_task(consume())

@app.get("/")
async def home():
    return {"service": "payment service running"}