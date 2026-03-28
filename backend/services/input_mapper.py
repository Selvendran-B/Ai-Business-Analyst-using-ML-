class InputMapper:
    """
    Converts human inputs into ML-ready feature vectors
    """

    SECTOR_MAP = {
        "textile": 2,
        "garments": 3,
        "food": 4,
        "retail": 5,
        "it": 6
    }

    CITY_MAP = {
        "tiruppur": 1,
        "coimbatore": 0
    }

    @staticmethod
    def map_to_features(
        investment_lakhs: float,
        city: str,
        sector: str
    ):
        # Simple heuristic assumptions
        revenue = investment_lakhs * 1.5
        expense = investment_lakhs * 0.9

        demand = 80
        competition = 45
        risk = 30
        opportunity = 75
        growth = 10

        return [
            investment_lakhs,
            revenue,
            expense,
            demand,
            competition,
            risk,
            opportunity,
            growth,
            InputMapper.SECTOR_MAP.get(sector.lower(), 0),
            InputMapper.CITY_MAP.get(city.lower(), 0)
        ]
