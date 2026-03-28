import pandas as pd
from backend.services.dataset_loader import DataLoader
from backend.services.preprocess import Preprocess

class RealAnalyticsEngine:

    def __init__(self):
        loader = DataLoader()
        preprocess = Preprocess()

        tiruppur, coimbatore = loader.load_real_data()

        self.tiruppur = preprocess.preprocess(tiruppur)
        self.coimbatore = preprocess.preprocess(coimbatore)

        self.tiruppur["city"] = "Tiruppur"
        self.coimbatore["city"] = "Coimbatore"

        self.df = pd.concat([self.tiruppur, self.coimbatore], ignore_index=True)

        # Ensure date parsing
        self.df["registrationdate"] = pd.to_datetime(
            self.df["registrationdate"], errors="coerce"
        )

    # -----------------------------
    # MSME COUNT
    # -----------------------------
    def msme_count(self, city: str):
        return int(
            self.df[self.df["city"].str.lower() == city.lower()].shape[0]
        )

    # -----------------------------
    # TOP ACTIVITIES
    # -----------------------------
    def top_activities(self, city: str, n=10):
        df = self.df[self.df["city"].str.lower() == city.lower()]
        return df["activities"].value_counts().head(n).to_dict()

    # -----------------------------
    # REGISTRATION TREND (YEAR)
    # -----------------------------
    def registration_trend(self, city: str):
        df = self.df[self.df["city"].str.lower() == city.lower()]
        df = df.dropna(subset=["registrationdate"])

        trend = (
            df["registrationdate"]
            .dt.year
            .value_counts()
            .sort_index()
        )

        return trend.to_dict()
