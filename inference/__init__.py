import os
import pickle
import sys

import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(".."))
from config.settings import Settings


from pathlib import Path

settings = Settings()


ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "artifacts" / "models" / "random_forest.pkl"
BIN_ENC_PATH = ROOT / "artifacts" / "encoders" / "binary_encoders.pkl"
OHE_PATH = ROOT / "artifacts" / "encoders" / "ohe_encoder.pkl"


class Infer:

    def __init__(self, data):
        self.df = pd.DataFrame(data)

        # Load the model
        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)

    def drop_columns(self):
        self.df = self.df.drop(columns=settings.drop_cols)
        return self.df

    def fillna(self):

        self.df[settings.binary_cols] = self.df[settings.binary_cols].fillna(
            self.df[settings.binary_cols].mode().iloc[0]
        )

        # self.df[settings.category_cols] = self.df[settings.category_cols].fillna(
        #     self.df[settings.category_cols].mode().iloc[0]
        # )

        # Fill categoricals: mode per column, then fallback to "MISSING", and force string dtype
        cat = self.df[settings.category_cols].copy()

        modes = cat.mode(dropna=True)  # one row with per-column modes (may be empty)
        if not modes.empty:
            cat = cat.fillna(modes.iloc[0])  # use mode where available

        cat = cat.fillna("MISSING").astype(
            "string"
        )  # fallback + consistent dtype for OHE
        self.df[settings.category_cols] = cat

        # (optional) quiet the future warning about silent downcasting
        self.df.infer_objects(copy=False)

        self.df[settings.continous_cols] = self.df[settings.continous_cols].fillna(
            self.df[settings.continous_cols].median()
        )

        return self.df

    def encode_binary(self):

        with open(BIN_ENC_PATH, "rb") as f:
            encoders = pickle.load(f)

        for col, le in encoders.items():
            self.df[col] = le.transform(self.df[col])

        return self.df

    def one_hot_encoder(self):

        with open(OHE_PATH, "rb") as f:
            ohe = pickle.load(f)

        print(self.df)

        enc = ohe.transform(self.df[settings.category_cols])

        enc_cols = ohe.get_feature_names_out(settings.category_cols)
        enc_df = pd.DataFrame(enc, columns=enc_cols, index=self.df.index).astype(int)

        self.df = pd.concat(
            [self.df.drop(columns=settings.category_cols), enc_df], axis=1
        )

        return self.df

    def process_datetime(self):

        for col in settings.datetime_cols:

            self.df[col] = pd.to_datetime(self.df[col], format="mixed")

            self.df[f"{col}_year"] = self.df[col].dt.year
            self.df[f"{col}_month"] = self.df[col].dt.month
            self.df[f"{col}_day"] = self.df[col].dt.day
            self.df = self.df.drop(columns=[col])

        return self.df

    def preprocess(self):

        self.df = self.drop_columns()
        self.df = self.fillna()
        self.df = self.encode_binary()
        self.df = self.one_hot_encoder()
        self.df = self.process_datetime()

        return self.df

    def predict(self):

        X = self.preprocess()
        prediction = self.model.predict(X)
        return prediction.astype(int).tolist()
