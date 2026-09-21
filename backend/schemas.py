from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SignalPerformanceBase(BaseModel):
    evaluation_timestamp: Optional[datetime] = None
    exit_price: Optional[float] = None
    actual_return_percentage: Optional[float] = None
    is_accurate: Optional[bool] = None

class SignalPerformanceResponse(SignalPerformanceBase):
    id: str
    signal_id: str

    class Config:
        orm_mode = True

class SignalBase(BaseModel):
    ticker: str
    company_name: str
    raw_headline: str
    source_url: Optional[str] = None
    sentiment_label: str
    confidence_score: float
    simulated_return_impact: float
    is_spam: bool
    entry_price: Optional[float] = None
    industry: Optional[str] = None
    needs_clarification: bool = False

class SignalCreate(SignalBase):
    pass

class SignalResponse(SignalBase):
    id: str
    timestamp: datetime
    performance: Optional[SignalPerformanceResponse] = None

    class Config:
        orm_mode = True
