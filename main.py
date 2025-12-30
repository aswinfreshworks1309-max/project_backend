# main.py (root)
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import SessionLocal
from sqlalchemy import text
import os

load_dotenv()

from app.database import Base, engine
from app.routers import router as api_router

# create tables (dev only)
Base.metadata.create_all(bind=engine)



app = FastAPI(title="Bus Ticket Booking API")





from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bus Ticket Booking API is up"}
