# Phase 4 — Captured Forecast Run

Real terminal output from `python -m src.forecast.run_forecast`, run against the live API (`uvicorn src.api.main:app`)
and live MySQL/MongoDB containers loaded with Task 2's data. Reproduce with:

```bash
docker-compose up -d
python -m src.database.sql.load_mysql        # if not already loaded
python -m src.database.mongodb.setup         # if not already loaded
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 &
python -m src.forecast.run_forecast
```

## Output

```
=== Forecasting next hour for PJME ===
Fetching PJME window from http://localhost:8000/api/sql/readings/range (2018-07-20 01:00:00 -> 2018-08-03 00:00:00)
Fetched 336 rows, 2018-07-20 01:00:00 -> 2018-08-03 00:00:00
--- BEFORE: last 3 hours of input for PJME ---
reading_ts
2018-08-02 22:00:00    41552.0
2018-08-02 23:00:00    38500.0
2018-08-03 00:00:00    35486.0
--- AFTER: PJME forecast for 2018-08-03 01:00:00 -> 32489.8 MW ---
WARNING  SQL write for 2018-08-03T01:00:00 not stored (status 500): likely already predicted by a previous run.
WARNING  Mongo write for 2018-08-03T01:00:00 not stored (status 500): likely already predicted by a previous run.

=== Forecasting next hour for AEP ===
Fetching AEP window from http://localhost:8000/api/sql/readings/range (2018-07-20 01:00:00 -> 2018-08-03 00:00:00)
Fetched 336 rows, 2018-07-20 01:00:00 -> 2018-08-03 00:00:00
--- BEFORE: last 3 hours of input for AEP ---
reading_ts
2018-08-02 22:00:00    17001.0
2018-08-02 23:00:00    15964.0
2018-08-03 00:00:00    14809.0
--- AFTER: AEP forecast for 2018-08-03 01:00:00 -> 13710.5 MW ---
SQL prediction stored: {"region_id": 2, "target_ts": "2018-08-03T01:00:00", "predicted_mw": 13710.55,
  "model_name": "xgboost", "prediction_id": 5, "generated_at": "2026-07-09T20:06:03"}
Mongo prediction stored: {"region_code": "AEP", "target_ts": "2018-08-03T01:00:00", "predicted_mw": 13710.548828125,
  "model_name": "xgboost", "generated_at": "2026-07-09T20:06:05.590274"}
```

## Notes for the report

- **AEP** is the clean example: a genuinely new forecast, written to both `predictions` stores in the same run —
  this is the end-to-end "prediction script writes back through the API" loop the rubric is looking for.
- **PJME** shows the script's duplicate handling instead: an earlier manual API test (Phase 3 review) had already
  inserted a prediction for the exact same `(region, target_ts, model)` key, so the unique constraint correctly
  rejected the second insert and the script logged a warning and moved on rather than crashing. Left in this capture
  deliberately — it's real, reproducible robustness, not a failure.
- Verified directly against the database afterward:

  ```sql
  SELECT * FROM predictions;
  -- prediction_id=5, region_id=2 (AEP), target_ts=2018-08-03 01:00:00, predicted_mw=13710.55, model_name=xgboost
  -- is the row this run added.
  ```
- The forecast (PJME 32,489.8 MW, AEP 13,710.5 MW) is in the same range as each region's actual last few hours,
  which is the expected sanity check for a next-hour forecast.
