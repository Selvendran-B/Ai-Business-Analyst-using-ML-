from backend.services.dataset_loader import DataLoader
from backend.services.preprocess import Preprocess

class MergeEngine:
    """
    This engine DOES NOT row-merge datasets.
    It only loads and prepares them for usage.
    """

    def load_all(self):
        loader = DataLoader()
        preprocess = Preprocess()

        # Load datasets
        tiruppur, coimbatore = loader.load_real_data()
        synthetic = loader.load_synthetic_data()

        # Preprocess
        tiruppur = preprocess.preprocess(tiruppur)
        coimbatore = preprocess.preprocess(coimbatore)
        synthetic = preprocess.preprocess(synthetic)

        # Add city labels to real data
        tiruppur["city"] = "Tiruppur"
        coimbatore["city"] = "Coimbatore"

        return {
            "real": {
                "tiruppur": tiruppur,
                "coimbatore": coimbatore
            },
            "synthetic": synthetic
        }
