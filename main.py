# main.py (root)
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers import router as api_router
import os

# NOTE: creating tables at import time can cause serverless startup to attempt
# a DB connection and crash if the network is unreachable. Only create tables
# when explicitly requested (e.g. local development) by setting
# CREATE_TABLES=1 in the environment.

 


app = FastAPI(title="Bus Ticket Booking API")

from app import models

@app.get("/")
def root():
    return {"message": "Bus Ticket Booking API is up"}

@app.get("/api/init-db")
def init_db():
    try:
        from app.database import Base, engine
        Base.metadata.create_all(bind=engine)
        return {"message": "Database tables created successfully"}
    except Exception as e:
        return {"error": str(e)}

from fastapi.middleware.cors import CORSMiddleware

# Explicitly allow the frontend origin
origins = [
    "https://locotranz.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


