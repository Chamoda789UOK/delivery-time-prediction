import os

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from auth import get_current_user
from auth import router as auth_router
from database import get_db
from ml.predictor import info, predict_minutes
from models import Prediction, User
from schemas import PredictionRecord, PredictionRequest, PredictionResponse

app = FastAPI(title="Delivery Time Prediction API")

origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/model/info")
def model_info():
    return info


@app.post("/api/v1/predictions", response_model=PredictionResponse)
def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    area = "Metropolitian" if request.area == "Metropolitan" else request.area

    delivery = {
        "Agent_Age": request.agent_age,
        "Agent_Rating": request.agent_rating,
        "Weather": request.weather,
        "Traffic": request.traffic,
        "Vehicle": request.vehicle,
        "Area": area,
        "Category": request.category,
        "distance_km": request.distance_km,
        "order_hour": request.departure_time.hour,
        "day_of_week": request.departure_time.weekday(),
    }

    minutes = predict_minutes(delivery)

    record = Prediction(
        user_id=user.id,
        agent_age=request.agent_age,
        agent_rating=request.agent_rating,
        weather=request.weather,
        traffic=request.traffic,
        vehicle=request.vehicle,
        area=request.area,
        category=request.category,
        distance_km=request.distance_km,
        departure_time=request.departure_time,
        predicted_minutes=minutes,
        model_version=info["model_version"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return PredictionResponse(
        id=record.id,
        predicted_minutes=minutes,
        estimated_arrival=request.departure_time + timedelta(minutes=minutes),
        model_version=info["model_version"],
        note="This is an estimate, not a guaranteed arrival time.",
    )


@app.get("/api/v1/predictions", response_model=list[PredictionRecord])
def list_predictions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = (
        select(Prediction)
        .where(Prediction.user_id == user.id)
        .order_by(Prediction.id.desc())
        .limit(100)
    )
    return db.scalars(query).all()


@app.get("/api/v1/predictions/{prediction_id}", response_model=PredictionRecord)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    record = db.get(Prediction, prediction_id)
    if record is None or record.user_id != user.id:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return record

@app.get("/api/v1/analytics/overview")
def analytics_overview(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = db.execute(
        select(
            func.count(Prediction.id),
            func.avg(Prediction.predicted_minutes),
            func.min(Prediction.predicted_minutes),
            func.max(Prediction.predicted_minutes),
        ).where(Prediction.user_id == user.id)
    ).one()

    return {
        "total_predictions": row[0],
        "average_minutes": round(float(row[1]), 1) if row[1] else 0,
        "shortest_minutes": row[2] or 0,
        "longest_minutes": row[3] or 0,
    }


@app.get("/api/v1/analytics/delivery-performance")
def analytics_performance(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    def average_by(column):
        rows = db.execute(
            select(column, func.count(Prediction.id), func.avg(Prediction.predicted_minutes))
            .where(Prediction.user_id == user.id)
            .group_by(column)
        ).all()
        return [
            {"name": name, "count": count, "average_minutes": round(float(avg), 1)}
            for name, count, avg in rows
        ]

    return {
        "by_vehicle": average_by(Prediction.vehicle),
        "by_traffic": average_by(Prediction.traffic),
    }