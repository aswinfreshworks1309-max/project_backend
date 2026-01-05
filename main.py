# main.py (root)
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers import router as api_router
import os
load_dotenv()
 
from app import models

app = FastAPI(title="Bus Ticket Booking API")


@app.get("/")
def root():
    return {"message": "Bus Ticket Booking API is up"}

@app.get("/init-db")
def init_db():
    from app.database import DATABASE_URL, engine, Base
    if not DATABASE_URL:
        return {"error": "DATABASE_URL environment variable is not set."}
    
    masked_url = DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "URL set but Hidden"
    
    try:
        if engine is None:
            return {"error": "Engine is None. Database URL might be missing or invalid.", "detected_host": masked_url}
            
        Base.metadata.create_all(bind=engine)
        return {
            "message": "Database tables created successfully",
            "host": masked_url
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "trace": traceback.format_exc(),
            "detected_host": masked_url
        }

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


