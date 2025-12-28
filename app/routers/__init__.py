from fastapi import APIRouter
from .users import router as users
from .buses import router as buses
from .schedules import router as schedules
from .seats import router as seats
from .bookings import router as bookings
from .payments import router as payments

router = APIRouter()

router.include_router(users)
router.include_router(buses)
router.include_router(schedules)
router.include_router(seats)
router.include_router(bookings)
router.include_router(payments)
