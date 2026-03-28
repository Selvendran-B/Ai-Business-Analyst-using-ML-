from fastapi import APIRouter
from backend.services.real_analytics_engine import RealAnalyticsEngine

router = APIRouter()
engine = RealAnalyticsEngine()

@router.get("/real/msme-count/{city}")
def msme_count(city: str):
    return {
        "city": city,
        "msme_count": engine.msme_count(city)
    }

@router.get("/real/top-activities/{city}")
def top_activities(city: str):
    return engine.top_activities(city)

@router.get("/real/registration-trend/{city}")
def registration_trend(city: str):
    return engine.registration_trend(city)
