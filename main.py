# main.py (root)
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers import router as api_router
import os
 
app = FastAPI(title="Bus Ticket Booking API")


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://locotranz-git-main-aswins-projects-7ca69fa9.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")


