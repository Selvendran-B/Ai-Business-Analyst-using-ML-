import joblib
import numpy as np
from backend.services.real_analytics_engine import RealAnalyticsEngine


class MLService:

    def __init__(self):

        # ML models
        self.profit_model = joblib.load("backend/ml_models/model_profit.pkl")
        self.success_model = joblib.load("backend/ml_models/model_success.pkl")
        self.recommend_model = joblib.load("backend/ml_models/model_recommend.pkl")

        # MSME analytics engine
        self.real_engine = RealAnalyticsEngine()

        # Encoding maps
        self.city_map = {
            "Coimbatore": 0,
            "Tiruppur": 1
        }

        self.sector_map = {
            "Textile": 0,
            "Garments": 1,
            "Retail": 2,
            "Food Business": 3,
            "Logistics": 4,
            "Manufacturing": 5,
            "IT Services": 6,
            "Beauty & Salon": 7,
            "Automobile": 8,
            "Health & Wellness": 9,
            "Electronics": 10,
            "E-Commerce": 11
        }

    # ----------------------------------------
    # SMART BUSINESS → SECTOR MAPPING
    # ----------------------------------------
    def normalize_sector(self, sector: str):

        s = sector.lower()

        if any(x in s for x in ["tea", "coffee", "restaurant", "food", "hotel", "cafe", "bakery"]):
            return "Food Business"

        elif any(x in s for x in ["textile", "fabric", "cloth"]):
            return "Textile"

        elif any(x in s for x in ["garment", "tailor", "apparel"]):
            return "Garments"

        elif any(x in s for x in ["shop", "store", "retail"]):
            return "Retail"

        elif any(x in s for x in ["transport", "logistics", "delivery"]):
            return "Logistics"

        elif any(x in s for x in ["factory", "manufacturing"]):
            return "Manufacturing"

        elif any(x in s for x in ["software", "it", "development", "tech"]):
            return "IT Services"

        elif any(x in s for x in ["salon", "beauty", "spa"]):
            return "Beauty & Salon"

        elif any(x in s for x in ["automobile", "mechanic", "garage"]):
            return "Automobile"

        elif any(x in s for x in ["health", "clinic", "fitness"]):
            return "Health & Wellness"

        elif any(x in s for x in ["electronics", "mobile", "repair"]):
            return "Electronics"

        elif any(x in s for x in ["online", "ecommerce"]):
            return "E-Commerce"

        return sector

    # ----------------------------------------
    # MAIN BUSINESS ANALYSIS
    # ----------------------------------------
    def analyze_business(self, city: str, sector: str, investment: float):

        sector = self.normalize_sector(sector)

        city_encoded = self.city_map.get(city, 0)
        sector_encoded = self.sector_map.get(sector, self.sector_map["Retail"])
        # ----------------------------------------
        # REAL MSME DATA
        # ----------------------------------------

        total_msme = self.real_engine.msme_count(city)
        top_activities = self.real_engine.top_activities(city)

        # Detect sector competition
        sector_count = 0

        for act, count in top_activities.items():

            act_lower = act.lower()

            if sector.lower() in act_lower:
                sector_count += count

            # Food business grouping
            if sector == "Food Business":
                if any(x in act_lower for x in ["food", "restaurant", "tea", "catering"]):
                    sector_count += count

        # Competition %
        if total_msme > 0:
            competition_level = (sector_count / total_msme) * 100
        else:
            competition_level = 40

        # ----------------------------------------
        # REGISTRATION TREND
        # ----------------------------------------

        trend = self.real_engine.registration_trend(city)
        years = sorted(trend.keys())

        if len(years) >= 2:

            last = trend[years[-1]]
            prev = trend[years[-2]]

            growth_rate = ((last - prev) / prev) * 100

# smooth extreme values
            growth_rate = growth_rate * 0.5

            growth_rate = max(min(growth_rate, 15), -10)

        else:
            growth_rate = 5

        # ----------------------------------------
        # MARKET FEATURES
        # ----------------------------------------

        market_demand = 60 + (growth_rate / 5)

        risk_score = 40 + competition_level / 2

        opportunity_score = market_demand - (competition_level / 3)

        # ----------------------------------------
        # REVENUE MODEL
        # ----------------------------------------

        monthly_revenue = investment * (1.5 + growth_rate / 60)

        monthly_expense = monthly_revenue * (0.6 + competition_level / 250)

        # ----------------------------------------
        # ML FEATURE VECTOR
        # ----------------------------------------

        features = [
            investment,
            monthly_revenue,
            monthly_expense,
            market_demand,
            competition_level,
            risk_score,
            opportunity_score,
            growth_rate,
            sector_encoded,
            city_encoded
        ]

        predicted_profit = float(self.profit_model.predict([features])[0])

        success_probability = float(
            self.success_model.predict_proba([features])[0][1]
        )

        success_percent = success_probability * 100

        break_even_months = investment / predicted_profit if predicted_profit > 0 else 0

        # ----------------------------------------
        # CLUSTER RECOMMENDATION
        # ----------------------------------------

        cluster_group = int(self.recommend_model.predict([[
            investment,
            predicted_profit,
            market_demand,
            competition_level,
            risk_score
        ]])[0])

        # ----------------------------------------
        # RISK LEVEL CALCULATION
        # ----------------------------------------

        risk_index = (
            competition_level * 0.4 +
            (100 - success_percent) * 0.4 +
            abs(growth_rate) * 0.2
        )

        if risk_index > 70:
            risk_level = "High"
        elif risk_index > 40:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return {

            "city": city,
            "sector": sector,
            "investment_lakhs": investment,

            "predicted_monthly_profit_lakhs": round(predicted_profit, 2),

            "success_probability_percent": round(success_percent, 2),

            "break_even_months": round(break_even_months, 1),

            "risk_level": risk_level,

            "competition_index": round(competition_level, 2),

            "growth_rate_percent": round(growth_rate, 2),

            "cluster_group": cluster_group
        }