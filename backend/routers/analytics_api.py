from fastapi import APIRouter
from backend.services.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/analytics", tags=["Analytics"])

engine = AnalyticsEngine()


@router.get("/top-profit/{city}")
def top_profit(city: str):
    return engine.top_profitable_businesses(city)


@router.get("/best-sectors/{city}")
def best_sectors(city: str):
    return engine.best_sectors(city)


@router.get("/cost/{city}")
def cost(city: str):
    return engine.cost_analysis(city)


@router.get("/risk/{city}")
def risk(city: str):
    return engine.risk_vs_opportunity(city)


@router.get("/compare/{sector}")
def compare(sector: str):
    return engine.compare_cities(sector)
