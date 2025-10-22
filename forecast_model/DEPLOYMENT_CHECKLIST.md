# 🚀 Deployment Checklist

## ✅ **Pre-Deployment Requirements**

### **1. Database Setup**
- [ ] Run the unique constraint SQL:
  ```sql
  ALTER TABLE price_forecast_data 
  ADD CONSTRAINT unique_forecast 
  UNIQUE (material_id, location_id, model_name, forecast_date);
  ```

### **2. Files Included in Docker**
- [x] `lambda_handler.py` - Main Lambda function
- [x] `insert_forecast_data.py` - Database insert functionality
- [x] `requirements.txt` - Dependencies
- [x] `Dockerfile` - Updated to include insert_forecast_data.py

### **3. Dependencies**
- [x] All required packages in `requirements.txt`
- [x] N-BEATS support with darts and torch
- [x] Database query functionality

## 🎯 **Deployment Steps**

### **1. Build Docker Image**
```bash
docker build -t forecast-lambda .
```

### **2. Deploy to AWS Lambda**
```bash
# Use your existing deploy.py script
python deploy.py
```

### **3. Test Deployment**
```bash
# Test with specific model
{
    "material_id": "100724-000000",
    "location_id": "212",
    "model_name": "Random Forest"
}

# Test with best model (no model_name)
{
    "material_id": "100724-000000",
    "location_id": "212"
}
```

## 🔍 **Verification**

### **Expected Behavior:**
1. **Specific Model**: Stores with actual model name (e.g., "Random Forest")
2. **Best Model**: Stores with model_name = "Best"
3. **No Duplicates**: Updates existing records instead of creating duplicates
4. **Database Integration**: Forecasts are stored in `price_forecast_data` table

### **Response Format:**
```json
{
    "statusCode": 200,
    "body": {
        "material_id": "100724-000000",
        "forecast_values": [106.26, 104.14, 103.60, 114.40, 115.18, 116.77],
        "forecast_dates": ["2025-10-01", "2025-11-01", "2025-12-01", "2026-01-01", "2026-02-01", "2026-03-01"],
        "model_used": "Random Forest",
        "mape": 4.554,
        "model_details": "Random Forest with lags [1, 2, 3, 6, 12] + month/year features"
    }
}
```

## 🎉 **Ready for Deployment!**

The Lambda function is fully functional with:
- ✅ All 5 forecasting models
- ✅ Automatic best model selection
- ✅ Database integration with upsert logic
- ✅ No duplicate prevention
- ✅ Location_id support
- ✅ Error handling and fallbacks
