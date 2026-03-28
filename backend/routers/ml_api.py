from fastapi import APIRouter
from backend.services.ml_service import MLService

router = APIRouter(prefix="/ml", tags=["ML Models"])
ml = MLService()

@router.post("/predict/profit")
def predict_profit(payload: dict):
    profit = ml.predict_profit(payload["features"])
    return {"predicted_monthly_profit": round(profit, 2)}

@router.post("/predict/success")
def predict_success(payload: dict):
    prob = ml.predict_success(payload["features"])
    return {"success_probability": round(prob, 2)}

@router.post("/recommend/business")
def recommend_business(payload: dict):
    cluster = ml.recommend_cluster(payload["features"])
    return {"business_cluster": cluster}
