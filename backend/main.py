from fastapi import FastAPI
from backend.routers.dataset_api import router as dataset_router
from backend.routers.analytics_api import router as analytics_router
from backend.routers.ai_agent_api import router as ai_router
from backend.routers.real_analytics_api import router as real_analytics_router
from backend.routers.ml_api import router as ml_router
from backend.api.business_analysis import router as business_router

app = FastAPI()

app.include_router(dataset_router)
app.include_router(analytics_router)
app.include_router(ai_router)
app.include_router(real_analytics_router)
app.include_router(ml_router)
app.include_router(business_router)
@app.get("/")
def home():
    return {"message": "MSME Backend Running — Day 2 Complete!"}
