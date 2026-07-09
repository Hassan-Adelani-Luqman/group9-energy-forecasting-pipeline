"""Task 4 - forecast script (Member 4).

fetch -> preprocess (reuse Phase 1's feature pipeline) -> load model -> predict -> write
back through the Phase 3 API. Run with:

    python -m src.forecast.run_forecast                  # both regions
    python -m src.forecast.run_forecast --region PJME     # one region
"""

import logging
from datetime import timedelta

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("forecast")

SQL_REGION_IDS = {"PJME": 1, "AEP": 2}
WINDOW_HOURS = 24 * 14  # 14 days of history - covers lag_168h plus headroom


def get_latest_timestamp(api_base: str, region_code: str) -> pd.Timestamp:
    """The dataset is historical (frozen at 2018-08-03), so "now" is wall-clock
    time, not data time - anchor the forecast on the latest reading actually in
    the DB rather than datetime.now(), or the range fetch below would come back
    empty."""
    url = f"{api_base}/api/sql/readings/latest"
    resp = requests.get(url, params={"region_id": SQL_REGION_IDS[region_code]}, timeout=30)
    resp.raise_for_status()
    return pd.Timestamp(resp.json()["reading_ts"])


def fetch_window(api_base: str, region_code: str, end_ts: pd.Timestamp) -> pd.DataFrame:
    start_ts = end_ts - timedelta(hours=WINDOW_HOURS - 1)
    url = f"{api_base}/api/sql/readings/range"
    params = {
        "region_id": SQL_REGION_IDS[region_code],
        "start_date": start_ts.isoformat(),
        "end_date": end_ts.isoformat(),
    }
    log.info(f"Fetching {region_code} window from {url} ({start_ts} -> {end_ts})")
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    rows = resp.json()

    if not rows:
        raise RuntimeError(
            f"No readings returned for {region_code} in [{start_ts}, {end_ts}]. "
            "Has data been loaded into MySQL via src/database/sql/load_mysql.py?"
        )

    df = pd.DataFrame(rows)
    df["reading_ts"] = pd.to_datetime(df["reading_ts"])
    df = df.sort_values("reading_ts").set_index("reading_ts")
    log.info(f"Fetched {len(df)} rows, {df.index.min()} -> {df.index.max()}")
    return df


if __name__ == "__main__":
    # temporary manual smoke test - replaced by the full pipeline + argparse next
    latest = get_latest_timestamp("http://localhost:8000", "PJME")
    window = fetch_window("http://localhost:8000", "PJME", latest)
    print(window[["mw"]].tail())
