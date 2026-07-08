# Phase 3 API Examples

This document captures example request/response pairs for both the MySQL (SQL) and MongoDB endpoints.

## MySQL Endpoints

### 1. Get Latest Reading (GET `/api/sql/readings/latest?region_id=1`)

**Request:**
```http
GET /api/sql/readings/latest?region_id=1 HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "region_id": 1,
  "reading_ts": "2018-08-03T00:00:00",
  "mw": 32950.5,
  "lag_1h": 33100.2,
  "lag_24h": 32800.1,
  "lag_168h": 33000.0,
  "rolling_mean_24h": 32500.4,
  "rolling_mean_7d": 32100.8,
  "rolling_std_24h": 500.2,
  "split": "test",
  "reading_id": 145224
}
```

### 2. Create Prediction (POST `/api/sql/predictions`)

**Request:**
```http
POST /api/sql/predictions HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "region_id": 1,
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 33150.0,
  "model_name": "xgboost"
}
```

**Response (200 OK):**
```json
{
  "region_id": 1,
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 33150.0,
  "model_name": "xgboost",
  "prediction_id": 1,
  "generated_at": "2026-07-08T16:00:00"
}
```

## MongoDB Endpoints

### 1. Get Daily Reading Document (GET `/api/mongo/readings/PJME/2018-08-03`)

**Request:**
```http
GET /api/mongo/readings/PJME/2018-08-03 HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "region_code": "PJME",
  "region_name": "PJM East",
  "date": "2018-08-03T00:00:00",
  "day_of_week": 4,
  "is_weekend": 0,
  "is_holiday": 0,
  "daily_stats": {
    "avg_mw": 32950.5,
    "min_mw": 28000.0,
    "max_mw": 35000.0,
    "peak_hour": 17,
    "n_hours": 24
  },
  "hourly_readings": [
    {
      "hour": 0,
      "ts": "2018-08-03T00:00:00",
      "mw": 32950.5,
      "lag_1h": 33100.2,
      "lag_24h": 32800.1,
      "lag_168h": 33000.0,
      "rolling_mean_24h": 32500.4,
      "rolling_mean_7d": 32100.8,
      "rolling_std_24h": 500.2,
      "split": "test"
    }
  ]
}
```

### 2. Create Prediction (POST `/api/mongo/predictions`)

**Request:**
```http
POST /api/mongo/predictions HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "region_code": "PJME",
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 33150.0,
  "model_name": "xgboost"
}
```

**Response (200 OK):**
```json
{
  "region_code": "PJME",
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 33150.0,
  "model_name": "xgboost",
  "generated_at": "2026-07-08T16:05:00"
}
```
