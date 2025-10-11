from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReadingCreate(BaseModel):
    heart_rate: int = Field(gt=30, lt=220)
    spo2: Optional[float] = Field(default=None, gt=0, lt=100)
    signal_quality: Optional[str] = None
    timestamp: datetime

class ReadingResponse(BaseModel):
    id: int
    heart_rate: int
    spo2: Optional[float]
    signal_quality: Optional[str]
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnomalyResponse(BaseModel):
    id: int
    reading_id: int
    anomaly_type: str
    severity: str
    description: Optional[str]
    detected_at: datetime
    
    class Config:
        from_attributes = True