import pandas as pd
from backend.services.merge_engine import MergeEngine


class AnalyticsEngine:
    """
    Analytics works ONLY on synthetic dataset
    (because real MSME data has no profit / risk fields)
    """

    def __init__(self):
        data = MergeEngine().load_all()
        self.df = data["synthetic"]   # ✅ synthetic dataset only

    # -------------------------------------------------
    # JSON SAFE CLEANER (prevents NaN / inf errors)
    # -------------------------------------------------
    def _clean_json(self, obj):
        if isinstance(obj, float):
            if pd.isna(obj) or obj in [float("inf"), float("-inf")]:
                return None
            return obj

        if isinstance(obj, dict):
            return {k: self._clean_json(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self._clean_json(v) for v in obj]

        return obj

    # -------------------------------------------------
    # City filter helper
    # -------------------------------------------------
    def _get_city_df(self, city: str):
        return self.df[
            self.df["city"].astype(str).str.lower() == city.lower()
        ]

    # -------------------------------------------------
    # Top profitable businesses
    # -------------------------------------------------
    def top_profitable_businesses(self, city: str, n: int = 5):
        df = self._get_city_df(city)
        df = df.sort_values(by="monthly_profit_lakhs", ascending=False)
        return self._clean_json(df.head(n).to_dict(orient="records"))

    # -------------------------------------------------
    # Best business sectors
    # -------------------------------------------------
    def best_sectors(self, city: str):
        df = self._get_city_df(city)
        sector_stats = (
            df.groupby("business_sector")["monthly_profit_lakhs"]
              .mean()
              .sort_values(ascending=False)
        )
        return self._clean_json(sector_stats.to_dict())

    # -------------------------------------------------
    # Cost analysis
    # -------------------------------------------------
    def cost_analysis(self, city: str):
        df = self._get_city_df(city)
        return self._clean_json({
            "avg_investment": round(df["investment_required_lakhs"].mean(), 2),
            "avg_expense": round(df["monthly_expense_lakhs"].mean(), 2),
            "avg_revenue": round(df["monthly_revenue_lakhs"].mean(), 2),
        })

    # -------------------------------------------------
    # Risk vs Opportunity
    # -------------------------------------------------
    def risk_vs_opportunity(self, city: str):
        df = self._get_city_df(city)
        return self._clean_json({
            "avg_risk": round(df["risk_score"].mean(), 2),
            "avg_opportunity": round(df["opportunity_score"].mean(), 2),
            "avg_success_probability": round(
                df["business_success_probability"].mean(), 2
            ),
        })

    # -------------------------------------------------
    # Compare cities for a sector
    # -------------------------------------------------
    def compare_cities(self, sector: str):
        df = self.df[
            self.df["business_sector"].astype(str).str.lower()
            == sector.lower()
        ]
        result = df.groupby("city")["monthly_profit_lakhs"].mean()
        return self._clean_json(result.to_dict())
