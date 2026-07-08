# Phase 3 API Examples

This document captures example request/response pairs for both the MySQL (SQL) and MongoDB endpoints based on actual loaded data.

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
  "mw": 31626.0,
  "lag_1h": 34456.0,
  "lag_24h": 33530.0,
  "lag_168h": 34332.0,
  "rolling_mean_24h": 33855.5,
  "rolling_mean_7d": 32934.5298,
  "rolling_std_24h": 3485.7952,
  "split": "train",
  "region_id": 1,
  "reading_id": 24,
  "reading_ts": "2002-01-09T23:00:00"
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
  "predicted_mw": 32950.5,
  "model_name": "xgboost"
}
```

**Response (200 OK):**
```json
{
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 32950.5,
  "model_name": "xgboost",
  "generated_at": "2026-07-07T00:00:00",
  "region_id": 1,
  "prediction_id": 1
}
```

## MongoDB Endpoints

### 1. Get Daily Reading Document (GET `/api/mongo/readings/PJME/2002-01-09`)

**Request:**
```http
GET /api/mongo/readings/PJME/2002-01-09 HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
  "region_code": "PJME",
  "region_name": "PJM East",
  "date": "2002-01-09T00:00:00",
  "day_of_week": 2,
  "is_weekend": 0,
  "is_holiday": 0,
  "daily_stats": {
    "avg_mw": 33776.17,
    "min_mw": 27759.0,
    "max_mw": 38111.0,
    "peak_hour": 19,
    "n_hours": 24
  },
  "hourly_readings": [
    {
      "hour": 0,
      "ts": "2002-01-09T00:00:00",
      "mw": 30943.0,
      "lag_1h": 33530.0,
      "lag_24h": 31187.0,
      "lag_168h": 29563.0,
      "rolling_mean_24h": 34362.9167,
      "rolling_mean_7d": 32987.7619,
      "rolling_std_24h": 3569.4543,
      "split": "train"
    },
    {
      "hour": 1,
      "ts": "2002-01-09T01:00:00",
      "mw": 29082.0,
      "lag_1h": 30943.0,
      "lag_24h": 29445.0,
      "lag_168h": 28121.0,
      "rolling_mean_24h": 34352.75,
      "rolling_mean_7d": 32995.9762,
      "rolling_std_24h": 3579.2275,
      "split": "train"
    },
    {
      "hour": 2,
      "ts": "2002-01-09T02:00:00",
      "mw": 28154.0,
      "lag_1h": 29082.0,
      "lag_24h": 28670.0,
      "lag_168h": 27437.0,
      "rolling_mean_24h": 34337.625,
      "rolling_mean_7d": 33001.6964,
      "rolling_std_24h": 3601.5655,
      "split": "train"
    },
    {
      "hour": 3,
      "ts": "2002-01-09T03:00:00",
      "mw": 27829.0,
      "lag_1h": 28154.0,
      "lag_24h": 28375.0,
      "lag_168h": 27301.0,
      "rolling_mean_24h": 34316.125,
      "rolling_mean_7d": 33005.9643,
      "rolling_std_24h": 3638.2237,
      "split": "train"
    },
    {
      "hour": 4,
      "ts": "2002-01-09T04:00:00",
      "mw": 27759.0,
      "lag_1h": 27829.0,
      "lag_24h": 28542.0,
      "lag_168h": 27533.0,
      "rolling_mean_24h": 34293.375,
      "rolling_mean_7d": 33009.1071,
      "rolling_std_24h": 3678.4735,
      "split": "train"
    },
    {
      "hour": 5,
      "ts": "2002-01-09T05:00:00",
      "mw": 28308.0,
      "lag_1h": 27759.0,
      "lag_24h": 29261.0,
      "lag_168h": 28405.0,
      "rolling_mean_24h": 34260.75,
      "rolling_mean_7d": 33010.4524,
      "rolling_std_24h": 3734.7432,
      "split": "train"
    },
    {
      "hour": 6,
      "ts": "2002-01-09T06:00:00",
      "mw": 30169.0,
      "lag_1h": 28308.0,
      "lag_24h": 31348.0,
      "lag_168h": 30748.0,
      "rolling_mean_24h": 34221.0417,
      "rolling_mean_7d": 33009.875,
      "rolling_std_24h": 3794.7959,
      "split": "train"
    },
    {
      "hour": 7,
      "ts": "2002-01-09T07:00:00",
      "mw": 34261.0,
      "lag_1h": 30169.0,
      "lag_24h": 35335.0,
      "lag_168h": 34725.0,
      "rolling_mean_24h": 34171.9167,
      "rolling_mean_7d": 33006.4286,
      "rolling_std_24h": 3840.956,
      "split": "train"
    },
    {
      "hour": 8,
      "ts": "2002-01-09T08:00:00",
      "mw": 36714.0,
      "lag_1h": 34261.0,
      "lag_24h": 37841.0,
      "lag_168h": 37313.0,
      "rolling_mean_24h": 34127.1667,
      "rolling_mean_7d": 33003.6667,
      "rolling_std_24h": 3833.0644,
      "split": "train"
    },
    {
      "hour": 9,
      "ts": "2002-01-09T09:00:00",
      "mw": 36494.0,
      "lag_1h": 36714.0,
      "lag_24h": 37417.0,
      "lag_168h": 37322.0,
      "rolling_mean_24h": 34080.2083,
      "rolling_mean_7d": 33000.1012,
      "rolling_std_24h": 3792.2749,
      "split": "train"
    },
    {
      "hour": 10,
      "ts": "2002-01-09T10:00:00",
      "mw": 36417.0,
      "lag_1h": 36494.0,
      "lag_24h": 36824.0,
      "lag_168h": 37035.0,
      "rolling_mean_24h": 34041.75,
      "rolling_mean_7d": 32995.1726,
      "rolling_std_24h": 3761.52,
      "split": "train"
    },
    {
      "hour": 11,
      "ts": "2002-01-09T11:00:00",
      "mw": 36529.0,
      "lag_1h": 36417.0,
      "lag_24h": 36504.0,
      "lag_168h": 36758.0,
      "rolling_mean_24h": 34024.7917,
      "rolling_mean_7d": 32991.494,
      "rolling_std_24h": 3749.3289,
      "split": "train"
    },
    {
      "hour": 12,
      "ts": "2002-01-09T12:00:00",
      "mw": 36181.0,
      "lag_1h": 36529.0,
      "lag_24h": 35741.0,
      "lag_168h": 36284.0,
      "rolling_mean_24h": 34025.8333,
      "rolling_mean_7d": 32990.131,
      "rolling_std_24h": 3750.051,
      "split": "train"
    },
    {
      "hour": 13,
      "ts": "2002-01-09T13:00:00",
      "mw": 35698.0,
      "lag_1h": 36181.0,
      "lag_24h": 35158.0,
      "lag_168h": 35548.0,
      "rolling_mean_24h": 34044.1667,
      "rolling_mean_7d": 32989.5179,
      "rolling_std_24h": 3759.8634,
      "split": "train"
    },
    {
      "hour": 14,
      "ts": "2002-01-09T14:00:00",
      "mw": 35342.0,
      "lag_1h": 35698.0,
      "lag_24h": 34591.0,
      "lag_168h": 34978.0,
      "rolling_mean_24h": 34066.6667,
      "rolling_mean_7d": 32990.4107,
      "rolling_std_24h": 3768.4247,
      "split": "train"
    },
    {
      "hour": 15,
      "ts": "2002-01-09T15:00:00",
      "mw": 34750.0,
      "lag_1h": 35342.0,
      "lag_24h": 34078.0,
      "lag_168h": 34304.0,
      "rolling_mean_24h": 34097.9583,
      "rolling_mean_7d": 32992.5774,
      "rolling_std_24h": 3776.0781,
      "split": "train"
    },
    {
      "hour": 16,
      "ts": "2002-01-09T16:00:00",
      "mw": 34709.0,
      "lag_1h": 34750.0,
      "lag_24h": 34006.0,
      "lag_168h": 34169.0,
      "rolling_mean_24h": 34125.9583,
      "rolling_mean_7d": 32995.2321,
      "rolling_std_24h": 3778.4145,
      "split": "train"
    },
    {
      "hour": 17,
      "ts": "2002-01-09T17:00:00",
      "mw": 35477.0,
      "lag_1h": 34709.0,
      "lag_24h": 35270.0,
      "lag_168h": 35674.0,
      "rolling_mean_24h": 34155.25,
      "rolling_mean_7d": 32998.4464,
      "rolling_std_24h": 3780.1686,
      "split": "train"
    },
    {
      "hour": 18,
      "ts": "2002-01-09T18:00:00",
      "mw": 37984.0,
      "lag_1h": 35477.0,
      "lag_24h": 38779.0,
      "lag_168h": 39532.0,
      "rolling_mean_24h": 34163.875,
      "rolling_mean_7d": 32997.2738,
      "rolling_std_24h": 3783.0577,
      "split": "train"
    },
    {
      "hour": 19,
      "ts": "2002-01-09T19:00:00",
      "mw": 38111.0,
      "lag_1h": 37984.0,
      "lag_24h": 39450.0,
      "lag_168h": 40002.0,
      "rolling_mean_24h": 34130.75,
      "rolling_mean_7d": 32988.0595,
      "rolling_std_24h": 3744.1707,
      "split": "train"
    },
    {
      "hour": 20,
      "ts": "2002-01-09T20:00:00",
      "mw": 37316.0,
      "lag_1h": 38111.0,
      "lag_24h": 38898.0,
      "lag_168h": 39484.0,
      "rolling_mean_24h": 34074.9583,
      "rolling_mean_7d": 32976.8036,
      "rolling_std_24h": 3670.7184,
      "split": "train"
    },
    {
      "hour": 21,
      "ts": "2002-01-09T21:00:00",
      "mw": 36319.0,
      "lag_1h": 37316.0,
      "lag_24h": 38178.0,
      "lag_168h": 38693.0,
      "rolling_mean_24h": 34009.0417,
      "rolling_mean_7d": 32963.8988,
      "rolling_std_24h": 3593.7406,
      "split": "train"
    },
    {
      "hour": 22,
      "ts": "2002-01-09T22:00:00",
      "mw": 34456.0,
      "lag_1h": 36319.0,
      "lag_24h": 36282.0,
      "lag_168h": 37016.0,
      "rolling_mean_24h": 33931.5833,
      "rolling_mean_7d": 32949.7679,
      "rolling_std_24h": 3519.2393,
      "split": "train"
    },
    {
      "hour": 23,
      "ts": "2002-01-09T23:00:00",
      "mw": 31626.0,
      "lag_1h": 34456.0,
      "lag_24h": 33530.0,
      "lag_168h": 34332.0,
      "rolling_mean_24h": 33855.5,
      "rolling_mean_7d": 32934.5298,
      "rolling_std_24h": 3485.7952,
      "split": "train"
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
  "predicted_mw": 32950.5,
  "model_name": "xgboost"
}
```

**Response (200 OK):**
```json
{
  "region_code": "PJME",
  "target_ts": "2018-08-03T01:00:00",
  "predicted_mw": 32950.5,
  "model_name": "xgboost",
  "generated_at": "2026-07-07T00:00:00"
}
```
