from fastapi import APIRouter
from backend.services.dataset_loader import DataLoader

router = APIRouter()
loader = DataLoader()

@router.get("/datasets/list")
def list_datasets():
    tiruppur, coimbatore = loader.load_real_data()
    synthetic = loader.load_synthetic_data()

    return {
        "real_datasets": ["msme_real_tiruppur.csv", "msme_real_coimbatore.csv"],
        "synthetic_datasets": ["business_master_dataset.csv"],
        "counts": {
            "tiruppur": len(tiruppur),
            "coimbatore": len(coimbatore),
            "synthetic": len(synthetic)
        }
    }


@router.get("/datasets/summary/{city}")
def dataset_summary(city: str):

    if city.lower() == "tiruppur":
        tiruppur, _ = loader.load_real_data()
        return loader.summary(tiruppur)

    if city.lower() == "coimbatore":
        _, coimbatore = loader.load_real_data()
        return loader.summary(coimbatore)

    return {"error": "City not found"}


@router.get("/datasets/search")
def search_business(business: str):

    synthetic = loader.load_synthetic_data()

    result = synthetic[synthetic["business_sector"].str.contains(business, case=False)]

    return {
        "search_keyword": business,
        "matched_rows": len(result),
        "sample": result.head(5).to_dict(orient="records")
    }
