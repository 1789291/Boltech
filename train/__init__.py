import os
import sys

import pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn import metrics

sys.path.append(os.path.abspath(".."))
from config.settings import Settings

settings = Settings()


class Train:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def X_y(self):
        target = settings.target_col[0]
        self.y = self.df[target]
        self.X = self.df.drop(columns=[target])
        return self.X, self.y

    def split_data(self, X, y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=settings.test_size,
            random_state=settings.random_state,
            stratify=y,
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_model(self):
        self.model = RandomForestClassifier(random_state=settings.random_state)
        self.model.fit(self.X_train, self.y_train)

        model_path = "../artifacts/models/random_forest.pkl"
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)

        print(f"✅ Model saved at {model_path}")
        return self.model

    def score(self):
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)

        y_train_proba = self.model.predict_proba(self.X_train)[:, 1]
        y_test_proba = self.model.predict_proba(self.X_test)[:, 1]

        results = {
            "train": {
                "accuracy": metrics.accuracy_score(self.y_train, y_train_pred),
                "f1": metrics.f1_score(self.y_train, y_train_pred),
                "roc_auc": metrics.roc_auc_score(self.y_train, y_train_proba),
            },
            "test": {
                "accuracy": metrics.accuracy_score(self.y_test, y_test_pred),
                "f1": metrics.f1_score(self.y_test, y_test_pred),
                "roc_auc": metrics.roc_auc_score(self.y_test, y_test_proba),
            },
        }

        report = []
        for split in ["train", "test"]:
            report.append(f"=== {split.upper()} RESULTS ===")
            report.append(f"Accuracy : {results[split]['accuracy']:.4f}")
            report.append(f"F1-score : {results[split]['f1']:.4f}")
            report.append(f"ROC AUC  : {results[split]['roc_auc']:.4f}")
            report.append("")

        os.makedirs("../artifacts/metrics", exist_ok=True)
        out_path = "../artifacts/metrics/model_scores.txt"
        with open(out_path, "w") as f:
            f.write("\n".join(report))

        print(f"✅ Scores saved to {out_path}")
        return results

    def run(self):
        # Full training pipeline
        print("📌 Splitting features and target...")
        X, y = self.X_y()

        print("📌 Splitting into train/test...")
        self.split_data(X, y)

        print("📌 Training model...")
        self.train_model()

        print("📌 Evaluating model...")
        results = self.score()

        print("✅ Pipeline finished.")
        return results
