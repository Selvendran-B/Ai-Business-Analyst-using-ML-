import json
import re
from backend.llm.groq_client import GroqClient
from backend.llm.ollama_client import OllamaClient
from backend.services.analytics_engine import AnalyticsEngine
from backend.services.real_analytics_engine import RealAnalyticsEngine
from backend.services.ml_service import MLService
from backend.services.input_mapper import InputMapper


class BusinessAgent:
    def __init__(self):
        self.groq = GroqClient()
        self.ollama = OllamaClient()
        self.analytics = AnalyticsEngine()
        self.real = RealAnalyticsEngine()
        self.ml = MLService()
    def _extract_investment(self, q: str):
            match = re.search(r"invest\s+(\d+)", q)
            if match:
                return float(match.group(1))
            return 10.0  # fallback
    def _extract_sector(self, q: str):
            sectors = [
                "textile",
                "garments",
                "food",
                "retail",
                "it",
                "manufacturing",
                "logistics",
                "electronics"
            ]

            for s in sectors:
                if s in q:
                    return s

            return None

    # ============================
    # MAIN ENTRY
    # ============================
    def answer(self, query: str):
        q = query.lower()

        # ---------- REAL MSME FACTS ----------
        if "how many" in q and "msme" in q:
            city = self._get_city(q)
            data = {
                "city": city,
                "msme_count": self.real.msme_count(city)
            }
            return self._explain(data)

        if "top" in q and "activity" in q:
            city = self._get_city(q)
            data = self.real.top_activities(city)
            return self._explain(data)

        if "registration" in q and "trend" in q:
            city = self._get_city(q)
            data = self.real.registration_trend(city)
            return self._explain(data)

        # ---------- ANALYTICS ----------
        if "best" in q and "sector" in q:
            city = self._get_city(q)
            data = self.analytics.best_sectors(city)
            return self._explain(data)

        if "top" in q and "profit" in q:
            city = self._get_city(q)
            data = self.analytics.top_profitable_businesses(city)
            return self._explain(data)

        if "risk" in q:
            city = self._get_city(q)
            data = self.analytics.risk_vs_opportunity(city)
            return self._explain(data)

        if "compare" in q:
            sector = self._extract_sector(q)

            if not sector:
                return self._explain({"error": "Sector not found for comparison"})

            data = self.analytics.compare_cities(sector)
            return self._explain({
                "sector": sector,
                "comparison": data
            })

        # ---------- ML PREDICTIONS ----------
        if "invest" in q and "profit" in q:
            investment = self._extract_investment(q)
            sector = self._extract_sector(q)
            city = self._get_city(q)

            features = InputMapper.map_to_features(
                investment_lakhs=investment,
                city=city,
                sector=sector
            )

            profit = self.ml.predict_profit(features)

            return self._explain({
                "city": city,
                "sector": sector,
                "investment_lakhs": investment,
                "predicted_monthly_profit_lakhs": round(profit, 2)
            })



        if "success" in q or "chance" in q:
            features = self._default_features()
            prob = self.ml.predict_success(features)
            return self._explain({
                "success_probability": round(prob, 2)
            })

        # ---------- FALLBACK LLM ----------
        return self._llm_fallback(query)

    # ============================
    # HELPERS
    # ============================
    def _get_city(self, q: str):
        return "Tiruppur" if "tiruppur" in q else "Coimbatore"

    def _default_features(self):
        # TEMP fixed values (Day 8 → dynamic input)
        return [
            10,   # investment
            15,   # revenue
            9,    # expense
            80,   # demand
            40,   # competition
            30,   # risk
            75,   # opportunity
            10,   # growth
            2,    # sector encoded
            1     # city encoded
        ]

    def _explain(self, data):
        prompt = f"""
You are an expert MSME Business Consultant.

Here is the data:
{json.dumps(data, indent=2)}

Explain this in simple language.
Give practical business insight.
"""
        try:
            return self.groq.ask(prompt)
        except Exception:
            return self.ollama.ask(prompt)

    def _llm_fallback(self, query):
        prompt = f"""
You are an AI Business Consultant for MSMEs.

Question:
{query}
"""
        try:
            return self.groq.ask(prompt)
        except Exception:
            return self.ollama.ask(prompt)
