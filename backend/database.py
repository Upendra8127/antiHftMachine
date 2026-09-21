from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./antiHft.db"

from sqlalchemy import event

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Signal(Base):
    __tablename__ = "signals"

    id = Column(String, primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String, index=True) # Now stores dynamically extracted company name
    company_name = Column(String) # For legacy compatibility or full name mapping
    raw_headline = Column(String)
    source_url = Column(String, nullable=True)
    sentiment_label = Column(String) # BUY POSITION, SELL POSITION, HOLD
    confidence_score = Column(Float)
    simulated_return_impact = Column(Float)
    is_spam = Column(Boolean, default=False)
    entry_price = Column(Float, nullable=True)
    
    # V2 Specific fields
    industry = Column(String, nullable=True)
    needs_clarification = Column(Boolean, default=False)

    performance = relationship("SignalPerformance", back_populates="signal", uselist=False)

class SignalPerformance(Base):
    __tablename__ = "signal_performance"

    id = Column(String, primary_key=True, default=generate_uuid)
    signal_id = Column(String, ForeignKey("signals.id"))
    evaluation_timestamp = Column(DateTime, nullable=True)
    exit_price = Column(Float, nullable=True)
    actual_return_percentage = Column(Float, nullable=True)
    is_accurate = Column(Boolean, nullable=True)

    signal = relationship("Signal", back_populates="performance")

# Create tables
Base.metadata.create_all(bind=engine)
