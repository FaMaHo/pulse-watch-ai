from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class HeartRateReading(Base):
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True)
    heart_rate = Column(Integer, nullable=False)
    spo2 = Column(Float, nullable=True)
    signal_quality = Column(String, nullable=True)  # 'good', 'poor', etc.
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Anomaly(Base):
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    reading_id = Column(Integer, ForeignKey("readings.id"))
    anomaly_type = Column(String, nullable=False)  # 'tachycardia', 'bradycardia'
    severity = Column(String, nullable=False)      # 'low', 'medium', 'high'
    description = Column(String)
    detected_at = Column(DateTime, default=datetime.utcnow)