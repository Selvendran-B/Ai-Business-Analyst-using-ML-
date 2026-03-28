import pandas as pd
import numpy as np
class Preprocess:

    def clean_columns(self, df):
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

    def fill_missing(self, df):
    # Fix numeric columns
        for col in df.select_dtypes(include=['float', 'int']).columns:
            df[col] = df[col].replace([np.inf, -np.inf], None)
            df[col] = df[col].fillna(df[col].mean())

    # Fix string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna("Unknown")

        return df


    def preprocess(self, df):
        df = self.clean_columns(df)
        df = self.fill_missing(df)
        return df
