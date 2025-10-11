from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db
from anomaly_detector import detect_anomaly

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pulse Watch AI")

@app.get("/")
def root():
    return {"status": "running", "message": "Pulse Watch AI Backend"}

@app.post("/api/readings", response_model=schemas.ReadingResponse)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    # Save reading
    db_reading = models.HeartRateReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    # Check for anomalies
    anomaly = detect_anomaly(reading.heart_rate, reading.spo2 or 95.0)
    if anomaly:
        db_anomaly = models.Anomaly(
            reading_id=db_reading.id,
            **anomaly
        )
        db.add(db_anomaly)
        db.commit()
    
    return db_reading

@app.get("/api/readings", response_model=List[schemas.ReadingResponse])
def get_readings(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.HeartRateReading)\
        .order_by(models.HeartRateReading.id.desc())\
        .limit(limit)\
        .all()

@app.get("/api/readings/latest", response_model=schemas.ReadingResponse)
def get_latest(db: Session = Depends(get_db)):
    reading = db.query(models.HeartRateReading)\
        .order_by(models.HeartRateReading.id.desc())\
        .first()
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found")
    return reading

@app.get("/api/anomalies", response_model=List[schemas.AnomalyResponse])
def get_anomalies(db: Session = Depends(get_db)):
    return db.query(models.Anomaly)\
        .order_by(models.Anomaly.detected_at.desc())\
        .all()

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get basic statistics"""
    total_readings = db.query(models.HeartRateReading).count()
    total_anomalies = db.query(models.Anomaly).count()
    
    # Calculate average heart rate
    readings = db.query(models.HeartRateReading).all()
    avg_hr = sum(r.heart_rate for r in readings) / len(readings) if readings else 0
    
    return {
        "total_readings": total_readings,
        "total_anomalies": total_anomalies,
        "avg_heart_rate": round(avg_hr, 1)
    }