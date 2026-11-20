from ml.predictor import predict_minutes, info

delivery = {
    "Agent_Age": 30,
    "Agent_Rating": 4.7,
    "Weather": "Sunny",
    "Traffic": "Low",
    "Vehicle": "motorcycle",
    "Area": "Urban",
    "Category": "Electronics",
    "distance_km": 8.0,
    "order_hour": 14,
    "day_of_week": 2,
}

print(predict_minutes(delivery))
print(info["model_version"])