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

 

@app.get("/")
def root():
    return {"message": "Bus Ticket Booking API is up"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


