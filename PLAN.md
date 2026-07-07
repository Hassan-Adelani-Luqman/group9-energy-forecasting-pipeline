# Group 9 — Energy Forecasting Pipeline: Execution Plan

## Context

The repo `group9-energy-forecasting-pipeline` is currently **completely empty** (only `.git/`, no commits, no files). This is a 4-person coursework project (deadline Fri Jul 10, 2026, 11:59pm) building an end-to-end time series pipeline over PJM hourly energy consumption data: EDA/modeling → MySQL + MongoDB → FastAPI CRUD → forecast script that closes the loop by writing predictions back through the API.

Two rubric constraints shape how this plan should be executed, not just what gets built:
- Code quality is marked down if the submission "reads as AI-generated" with no individual fingerprint.
- Each of the 4 members needs ≥4 commits with clear messages tied to their own assigned role.

**Confirmed decisions:**
- Team roles stay as generic placeholders (Member 1: EDA/modeling, Member 2: databases, Member 3: API, Member 4: forecast script) — not yet assigned to real names.
- Docker is available locally → docker-compose for MySQL + MongoDB.
- Dataset acquisition (PJME + AEP Kaggle CSVs) is **manual**: each teammate downloads the CSVs from Kaggle themselves and places them in `data/raw/` during Phase 0 setup. No API credentials, no auto-download step in the notebook — this avoids every teammate needing a personal Kaggle API token just to run the EDA notebook.

This plan is meant to be handed to the team as-is (e.g. duplicated as `CLAUDE.md` at repo root) and executed phase-by-phase across separate sessions/branches per member.

## Approach

Execute in 5 phases, matching the roles table. Phase 0 (scaffold) is a prerequisite for everything else and should run first. Phases 1–4 then proceed largely in parallel per-owner, with one hard sync point at end of Day 1 (Member 1's processed data + Member 2's finalized schema unblock Members 3 and 4).

### Phase 0 — Repo Scaffold & Setup (prerequisite, run first)
Creates the skeleton every other phase builds on:
- Folder structure: `data/{raw,processed}`, `notebooks/`, `src/{preprocessing,models/artifacts,database/{sql,mongodb},api/routers,forecast}`, `reports/figures`, `docs/`
- `requirements.txt` (pandas, numpy, matplotlib, seaborn, statsmodels, scikit-learn, xgboost, holidays, sqlalchemy, pymysql, pymongo, fastapi, uvicorn, joblib, python-dotenv)
- `docker-compose.yml` (MySQL 8 + MongoDB 7)
- `.env.example` (DB connection settings only — host/port/user/password/db name for MySQL and Mongo), `.gitignore` (venv, `__pycache__`, `.env`, `data/raw/*.csv`, model artifacts if large)
- `README.md` stub (filled in incrementally as phases land)
- `PLAN.md` (this file) and/or `CLAUDE.md` pointing to it
- Empty placeholder files for each phase's key modules so branches don't collide on file *creation* (e.g. `src/preprocessing/clean.py`, `src/database/sql/schema.sql`, `src/api/main.py`, `src/forecast/run_forecast.py`)
- **Manual step for every teammate:** download the PJME and AEP hourly CSVs from the [Kaggle Hourly Energy Consumption dataset](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) and place them in `data/raw/` before running the notebook. `data/raw/*.csv` is gitignored, so this is a one-time local step per machine, not something committed.

### Phase 1 — EDA, Preprocessing & Modeling (Member 1)
- `notebooks/01_eda_and_preprocessing.ipynb`: load the manually-placed PJME + AEP CSVs from `data/raw/` (fail with a clear message if missing, pointing back to the Phase 0 download step). Dataset understanding (time range, frequency, missing-value/gap analysis with documented interpolation rule), distribution stats.
- ≥5 analytical questions with visuals + written interpretation; 2 must explicitly use lag features and moving averages (trend/STL, seasonality, weekday/weekend + holiday effect via the `holidays` package, ACF/lag-24h/168h correlation, 24h/7d rolling mean, cross-region correlation).
- `src/preprocessing/clean.py` (reindex to full hourly index, gap handling, dedupe) and `features.py` (calendar features + lag_1h/24h/168h + rolling_mean_24h/7d + rolling_std_24h).
- Chronological train/val/test split (never shuffle).
- Save processed data to `data/processed/` — this is the Day-1 handoff Members 2–4 are blocked on.
- `src/models/train.py` + `evaluate.py`: Linear Regression baseline, then XGBoost/RandomForest with `GridSearchCV`/`RandomizedSearchCV`; save winning model to `src/models/artifacts/`; fill in the experiment comparison table (RMSE/MAE/MAPE).

**Phase 1 status: complete** (branch `phase1-eda`). Notebook executed end-to-end, 6 analytical questions answered with figures in `reports/figures/`, processed CSVs exported to `data/processed/` (gitignored, regenerable from `data/raw/` via the notebook), and both model experiments run for both regions:

| Exp ID | Region | Model | Features | Key hyperparams | Val RMSE | Val MAE | Val MAPE | Test RMSE | Test MAE | Test MAPE |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | PJME | Linear Regression | calendar + lag_1h/24h/168h | — (baseline) | 1545.1 | 1212.2 | 3.63% | 1627.4 | 1349.2 | 3.84% |
| E2 | PJME | XGBoost | + rolling_mean_24h/7d, rolling_std_24h | `n_estimators=400, max_depth=5, learning_rate=0.1, subsample=0.7, colsample_bytree=0.85` (via RandomizedSearchCV) | 483.1 | 359.5 | 1.05% | 495.1 | 369.1 | 1.00% |
| E1 | AEP | Linear Regression | calendar + lag_1h/24h/168h | — (baseline) | 567.4 | 471.2 | 3.06% | 575.6 | 479.5 | 3.10% |
| E2 | AEP | XGBoost | + rolling_mean_24h/7d, rolling_std_24h | `n_estimators=400, max_depth=5, learning_rate=0.1, subsample=0.7, colsample_bytree=0.85` (via RandomizedSearchCV) | 175.4 | 135.7 | 0.86% | 178.3 | 137.5 | 0.87% |

XGBoost wins for both regions and is saved as `src/models/artifacts/{region}_winning_model.joblib`; the full table is also in `src/models/artifacts/experiment_results.csv`. Notable finding for the report: PJME and AEP are strongly correlated at the same hour with no meaningful lead/lag between them (Q6), and neither region shows a strong long-term STL trend (Q1) — seasonality, weekday/weekend, and lag structure are doing the real predictive work.

### Phase 2 — Databases (Member 2)
- `src/database/sql/schema.sql`: 4 tables (`regions`, `calendar_features`, `energy_readings`, `predictions`) with FKs and a unique `(region_id, reading_ts)` constraint.
- `docs/erd.mmd`: Mermaid ERD matching the schema.
- A load script to populate MySQL from Member 1's `data/processed/` output.
- `src/database/mongodb/setup.py` + `sample_documents.json`: document-per-region-per-day model with embedded `hourly_readings` and `daily_stats`, plus a parallel `predictions` collection.
- ≥3 required queries per DB, captured with results for the report (SQL: latest reading, avg-by-day-of-week join, 7-day rolling window function, date-range filter; Mongo: latest doc, `$group` monthly average, date-range filter, `$unwind` peak-hour lookup).

**Phase 2 status: complete** (merged via PR #2, branch `databases`). Schema, ERD, both loaders, and all queries verified
by actually running them against fresh containers — not just written:

- MySQL: 4-table 3NF schema (`regions`, `calendar_features`, `energy_readings`, `predictions`) applied cleanly;
  `load_mysql.py` loaded 145,224 PJME rows + 121,128 AEP rows. 5 queries run (exceeds the ≥3 minimum): latest record
  *(required)*, date-range *(required)*, avg-by-day-of-week join, 7-day rolling average via window function, peak
  hour per region. All-time peaks: PJME 62,009 MW (2006-08-02 17:00), AEP 25,695 MW (2008-10-20 14:00).
- MongoDB: document-per-region-per-day design (`energy_daily`) loaded 6,052 PJME + 5,048 AEP day-documents, plus an
  empty `predictions` collection for Phase 4. 4 queries run (exceeds the ≥3 minimum): latest document *(required)*,
  date-range *(required)*, `$group` monthly average, `$unwind` all-time-peak/peak-hour distribution — cross-checked
  against the SQL peak-hour result and matches exactly.
- Full captured query output for the report is in [`src/database/query_results.md`](src/database/query_results.md).
  Design rationale and reproduction steps are in [`src/database/README.md`](src/database/README.md).

### Phase 3 — CRUD API (Member 3)
- `src/api/main.py` + `routers/sql_routes.py` + `routers/mongo_routes.py` + `schemas.py` (FastAPI + Pydantic).
- Parallel endpoint sets for SQL and Mongo: POST/GET(list)/GET(latest)/GET(range)/GET(one)/PUT/DELETE on `readings`, plus POST on `predictions` for both backends.
- Can scaffold routing/config on Day 1 against placeholder data; wire real queries once Phase 2's schema + loaded data land.
- Smoke-test every endpoint via FastAPI's `/docs`; save example request/response pairs for the report.

### Phase 4 — Forecast Script (Member 4)
- `src/forecast/run_forecast.py`: fetch a trailing ~14-day window via the API's `/range` endpoint (not `/latest` alone — needed for `lag_168h`), run it through the **same** `src/preprocessing/features.py` from Phase 1 (import, don't reimplement), load the saved model from `src/models/artifacts/`, predict the next hour(s), POST the result to `/api/sql/predictions` and/or `/api/mongo/predictions`.
- Log a clear before/after (input window → prediction) for a report screenshot.
- Member 4 also compiles the final `reports/report.pdf` from all members' sections (problem definition, Task 1–4 write-ups, team contributions, limitations).

### Cross-cutting: Git workflow
One branch per member per phase (`phase1-eda`, `phase2-db`, `phase3-api`, `phase4-forecast`) merged via PR into `main`. Commit incrementally with specific messages (`feat: add lag and rolling-window features`, not `wip`/`final`) — this is what the ≥4-commits-per-person rubric row is actually checking for.

## Verification

- Phase 0 done correctly: `docker-compose up -d` brings up MySQL + Mongo cleanly; `pip install -r requirements.txt` succeeds; folder structure matches what Phases 1–4 expect; notebook gives a clear error (not a crash) if `data/raw/` CSVs are missing.
- Phase 1: notebook runs top-to-bottom once the CSVs are manually placed in `data/raw/`; processed CSV lands in `data/processed/`.
- Phase 2: `schema.sql` applies cleanly to a fresh MySQL container; load script populates it from Phase 1's output; all required queries return non-empty, sensible results.
- Phase 3: every endpoint reachable and functional via `/docs` against real loaded data.
- Phase 4: script runs end-to-end against the running API and a trained model artifact, and a new row appears in `predictions` (SQL and/or Mongo) after each run.
- Final: walk the full rubric checklist (dataset justification, ≥5 analytical questions with 2 lag/rolling, ≥2 modeling experiments with tuning, DB design + queries, CRUD both DBs, forecast script end-to-end, ≥4 commits per member, code quality) before submission.
