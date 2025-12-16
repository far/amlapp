# Usage:

## Install dependencies
```
uv sync
```
## Run with mock provider (default)
```
uv run uvicorn main:app --reload
```

## Run with real provider
```
AML_API_ACCESS_ID=your-access-id
AML_API_ACCESS_KEY=your-access-key uv run uvicorn main:app --reload
```

## Test the endpoint:

### Request

curl -X POST http://localhost:8000/check-address \
  -H "Content-Type: application/json" \
  -d '{"address": "0xf2e8e0761df9acda6d6b67a219ce41e522647e26", "currency": "ETH"}'

### Response

{"status":"success","risk_score":0.63,"risk_level":null,"categories":["Fake_Phishing","Harmony Horizon Bridge Exploiter"],"pdf_url":"/report/ETH0xf2e8e0761df9acda6d6b67a219ce41e522647e26"}

PDF report link in response is relative, so in our case URL will be "http://localhost:8000/report/ETH0xf2e8e0761df9acda6d6b67a219ce41e522647e26"

