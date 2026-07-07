# Group 9 — Energy Forecasting Pipeline

End-to-end time series pipeline for the [PJM Hourly Energy Consumption](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) dataset (PJME + AEP regions): EDA & forecasting models -> MySQL + MongoDB storage -> FastAPI CRUD -> forecast script that writes predictions back through the API.

See [PLAN.md](PLAN.md) for the full execution plan, phase breakdown, and rubric mapping.

## Team & Roles

| Member | Owns |
|---|---|
| 1 | EDA, preprocessing, modeling |
| 2 | SQL + MongoDB design & implementation |
| 3 | CRUD API for both databases |
| 4 | Forecast script; final report |

## Setup

1. Clone the repo and create a Python virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and adjust values if needed.
3. Start local MySQL + MongoDB:
   ```
   docker-compose up -d
   ```
4. Download the PJME and AEP CSVs from the [Kaggle dataset](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) and place them in `data/raw/`.
5. Run the EDA notebook: `notebooks/01_eda_and_preprocessing.ipynb`.

## Running the API

```
uvicorn src.api.main:app --reload
```
Docs available at `http://localhost:8000/docs`.

## Running the forecast script

```
python -m src.forecast.run_forecast
```
