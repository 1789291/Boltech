import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pickle

sys.path.append(os.path.abspath(".."))
from config.settings import Settings


settings = Settings()


class Preprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

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

        modes = cat.mode(dropna=True)          # one row with per-column modes (may be empty)
        if not modes.empty:
            cat = cat.fillna(modes.iloc[0])    # use mode where available

        cat = cat.fillna("MISSING").astype("string")  # fallback + consistent dtype for OHE
        self.df[settings.category_cols] = cat

        # (optional) quiet the future warning about silent downcasting
        self.df.infer_objects(copy=False)


        

        self.df[settings.continous_cols] = self.df[settings.continous_cols].fillna(
            self.df[settings.continous_cols].median()
        )

        return self.df

    def encode_binary(self):

        encoders = {}

        self.df[settings.target_col[0]] = self.df[settings.target_col[0]].map(
            settings.target_mapping
        )

        for col in settings.binary_cols:
            le = LabelEncoder()
            self.df[col] = le.fit_transform(self.df[col])
            encoders[col] = le

        with open("../artifacts/encoders/binary_encoders.pkl", "wb") as f:
            pickle.dump(encoders, f)

        return self.df

    def one_hot_encoder(self):

        os.makedirs("../artifacts/encoders", exist_ok=True)

        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

        X_cat = self.df[settings.category_cols]
        enc = ohe.fit_transform(X_cat)

        enc_cols = ohe.get_feature_names_out(settings.category_cols)
        enc_df = pd.DataFrame(enc, columns=enc_cols, index=self.df.index).astype(int)

        self.df = pd.concat(
            [self.df.drop(columns=settings.category_cols), enc_df], axis=1
        )

        with open("../artifacts/encoders/ohe_encoder.pkl", "wb") as f:
            pickle.dump(ohe, f)

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
