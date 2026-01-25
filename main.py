# main.py (root)
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers import router as api_router
import os
load_dotenv()
 
from app import models

# Create tables on startup
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

app = FastAPI(title="Bus Ticket Booking API")


# Recap: Root endpoint to check if the API is running.
@app.get("/") 
def root():
    return {"message": "Bus Ticket Booking API is up"}

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


