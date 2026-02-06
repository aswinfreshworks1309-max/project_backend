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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bus Ticket Booking API")

# Update CORS to be more permissive and robust
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://full-stack-project-git-main-aswins-projects-7ca69fa9.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Recap: Root endpoint to check if the API is running.
@app.get("/") 
def root():
    return {"message": "Bus Ticket Booking API is up"}

app.include_router(api_router)


