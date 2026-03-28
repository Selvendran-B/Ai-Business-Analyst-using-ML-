import pandas as pd
import os

DATA_DIR = os.path.join(os.getcwd(), "data")

class DataLoader:

    def load_real_data(self):
        tiruppur = pd.read_csv(f"{DATA_DIR}/real/msme_real_tiruppur.csv")
        coimbatore = pd.read_csv(f"{DATA_DIR}/real/msme_real_coimbatore.csv")
        return tiruppur, coimbatore

    def load_synthetic_data(self):
        synthetic = pd.read_csv(f"{DATA_DIR}/synthetic/business_master_dataset.csv")
        return synthetic

    def summary(self, df):
        return {
            "rows": len(df),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict()
        }
