"""Model training experiments for hourly energy demand forecasting.

Consumes the processed CSVs produced by notebooks/01_eda_and_preprocessing.ipynb
(data/processed/{region}_hourly_processed.csv), which already carry calendar
features, lag_1h/24h/168h, rolling_mean_24h/7d, rolling_std_24h, and a
chronological train/val/test split label.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.models.evaluate import compute_metrics

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "src" / "models" / "artifacts"

REGIONS = ["pjme", "aep"]
TARGET = "mw"
CALENDAR_LAG_FEATURES = [
    "hour", "day_of_week", "is_weekend", "is_holiday", "month",
    "lag_1h", "lag_24h", "lag_168h",
]
FULL_FEATURES = CALENDAR_LAG_FEATURES + [
    "rolling_mean_24h", "rolling_mean_7d", "rolling_std_24h",
]


def load_processed(region):
    path = PROCESSED_DIR / f"{region}_hourly_processed.csv"
    return pd.read_csv(path, index_col="datetime", parse_dates=True)


def get_split(df, split_name):
    return df.loc[df["split"] == split_name]


def train_linear_regression(df):
    """Experiment 1 (baseline): calendar + lag features only, no tuning."""
    train, val, test = (get_split(df, s) for s in ("train", "val", "test"))

    model = LinearRegression()
    model.fit(train[CALENDAR_LAG_FEATURES], train[TARGET])

    val_metrics = compute_metrics(val[TARGET], model.predict(val[CALENDAR_LAG_FEATURES]))
    test_metrics = compute_metrics(test[TARGET], model.predict(test[CALENDAR_LAG_FEATURES]))
    return model, val_metrics, test_metrics


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for region in REGIONS:
        df = load_processed(region)

        lr_model, lr_val, lr_test = train_linear_regression(df)
        rows.append({
            "region": region, "exp_id": "E1", "model": "LinearRegression",
            "features": "calendar+lag", "hyperparams": "-",
            "val_rmse": lr_val["rmse"], "val_mae": lr_val["mae"], "val_mape": lr_val["mape"],
            "test_rmse": lr_test["rmse"], "test_mae": lr_test["mae"], "test_mape": lr_test["mape"],
        })
        print(f"[{region}] E1 LinearRegression val={lr_val} test={lr_test}")

    results = pd.DataFrame(rows)
    results.to_csv(ARTIFACTS_DIR / "experiment_results.csv", index=False)
    print(results)


if __name__ == "__main__":
    main()
