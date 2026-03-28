from fastapi import APIRouter
from backend.services.ml_service import MLService

router = APIRouter()
ml = MLService()

@router.post("/analyze-business")
def analyze_business(data: dict):

    city = data.get("city")
    sector = data.get("sector")
    investment = float(data.get("investment"))

    result = ml.analyze_business(city, sector, investment)

    return result