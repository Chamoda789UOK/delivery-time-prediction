# AI-Based Logistics Delivery Time Prediction System

A web app that predicts delivery time in minutes using a Deep Neural Network regression model.

## Tech stack
- Model: TensorFlow / Keras, scikit-learn, pandas
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Frontend: React, TypeScript, Vite, Tailwind CSS, Recharts
- Tools: Docker, Docker Compose, GitHub Actions

## Dataset
Amazon Delivery Dataset from Kaggle (about 43,700 rows, 39,958 after cleaning).
Download it from Kaggle and check its licence on the dataset page. The data files are not stored in this repository.
It is food and parcel delivery data from India. It is not truck logistics data.

## Model
- Input features: agent age, agent rating, weather, traffic, vehicle, area, item category, distance (km), order hour, day of week
- Target: delivery time in minutes
- Architecture: Dense 128-64-32 (ReLU), 1 linear output, Adam, MSE loss, early stopping

## Test results (unseen test data)
| Model | MAE | RMSE | R² |
|---|---|---|---|
| DNN | 17.91 | 22.99 | 0.808 |
| Linear Regression | 25.66 | 32.52 | 0.617 |
| Random Forest | 17.68 | 22.94 | 0.809 |

Random Forest scored about the same as the DNN on this dataset.

## Run with Docker
1. Copy `.env.example` to `.env` and set your own values.
2. Run `docker compose up --build`
3. Open http://localhost:5173

Stop with `docker compose down`.

## Run tests
```
cd backend
pip install -r requirements.txt pytest httpx
python -m pytest -v
```

## Folders
- `training/` data preparation, training and evaluation scripts
- `backend/` FastAPI API and the saved model (`backend/ml`)
- `frontend/` React app

## Limitations
- Trained on delivery data from India, not truck logistics
- No real-time traffic or live weather
- Agent age and rating strongly affect predictions in this dataset
- Traffic has a smaller effect than expected in real life
- Results are estimates, not guaranteed arrival times