from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
import database, schemas, engine

app = FastAPI(title="antiHftMachine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "antiHftMachine API is running successfully!"}


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Background Tasks
def fetch_and_process_news():
    print(f"[{datetime.utcnow()}] Starting 5-min news ingestion cycle...")
    db = database.SessionLocal()
    articles = engine.fetch_rss_news()
    
    for article in articles:
        text = article['title'] + " " + article['summary']
        ticker, company_name, industry, needs_clarification = engine.extract_entities(text)
        
        if company_name:
            # Check if already processed recently to avoid duplicates
            recent = db.query(database.Signal).filter(
                database.Signal.raw_headline == article['title'],
                database.Signal.company_name == company_name
            ).first()
            
            if not recent:
                # 1. Pre-Sentiment Filter
                is_spam = engine.pre_sentiment_filter(text, company_name)
                
                # 2. AI Processing
                label, score, impact = engine.analyze_sentiment(text)
                
                # 3. Market Data
                current_price = engine.get_current_price(ticker) if ticker else None
                
                # 4. Save Signal
                db_signal = database.Signal(
                    ticker=ticker,
                    company_name=company_name,
                    raw_headline=article['title'],
                    source_url=article['link'],
                    sentiment_label=label,
                    confidence_score=score,
                    simulated_return_impact=impact,
                    is_spam=is_spam,
                    entry_price=current_price,
                    industry=industry,
                    needs_clarification=needs_clarification
                )
                db.add(db_signal)
                db.commit()
                db.refresh(db_signal)
                print(f"Stored Signal: {company_name} | {label} | Score: {score}")
    db.close()

def evaluate_eod_returns():
    print(f"[{datetime.utcnow()}] Starting EOD Return Evaluation...")
    db = database.SessionLocal()
    
    # Get all signals from today that don't have performance metrics yet
    today = datetime.utcnow().date()
    unevaluated_signals = db.query(database.Signal).outerjoin(database.SignalPerformance).filter(
        database.Signal.timestamp >= today,
        database.Signal.is_spam == False,
        database.SignalPerformance.id == None
    ).all()
    
    for signal in unevaluated_signals:
        if signal.entry_price:
            exit_price = engine.get_current_price(signal.ticker)
            if exit_price:
                actual_return = ((exit_price - signal.entry_price) / signal.entry_price) * 100
                
                # Accuracy logic
                is_accurate = False
                if signal.sentiment_label == 'BUY POSITION' and actual_return > 0:
                    is_accurate = True
                elif signal.sentiment_label == 'SELL POSITION' and actual_return < 0:
                    is_accurate = True
                    
                perf = database.SignalPerformance(
                    signal_id=signal.id,
                    evaluation_timestamp=datetime.utcnow(),
                    exit_price=exit_price,
                    actual_return_percentage=actual_return,
                    is_accurate=is_accurate
                )
                db.add(perf)
                db.commit()
                print(f"Evaluated EOD Return for {signal.ticker}: {actual_return}% | Accurate: {is_accurate}")
    db.close()


@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every 5 minutes for news
    scheduler.add_job(fetch_and_process_news, 'interval', minutes=5)
    # Run at EOD (e.g., 16:00 IST / 10:30 UTC for Indian Market)
    scheduler.add_job(evaluate_eod_returns, 'cron', hour=10, minute=30)
    scheduler.start()


# API Endpoints
@app.get("/api/signals", response_model=List[schemas.SignalResponse])
def get_signals(
    min_confidence: float = 0.0, 
    hide_neutral: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(database.Signal).filter(
        database.Signal.is_spam == False,
        database.Signal.confidence_score >= min_confidence
    )
    if hide_neutral:
        query = query.filter(database.Signal.sentiment_label != 'NEUTRAL')
        
    # Join with performance to get the full response
    signals = query.order_by(database.Signal.timestamp.desc()).all()
    return signals

@app.get("/api/kpis")
def get_kpis(db: Session = Depends(get_db)):
    signals = db.query(database.Signal).filter(database.Signal.is_spam == False).all()
    total = len(signals)
    pos = sum(1 for s in signals if s.sentiment_label == 'BUY POSITION')
    neg = sum(1 for s in signals if s.sentiment_label == 'SELL POSITION')
    
    # Calculate Overall Accuracy
    performances = db.query(database.SignalPerformance).all()
    evaluated = len(performances)
    accurate = sum(1 for p in performances if p.is_accurate)
    accuracy_rate = (accurate / evaluated * 100) if evaluated > 0 else 0.0
    
    return {
        "total_active_alerts": total,
        "net_positive_ratio": (pos / total * 100) if total > 0 else 0,
        "net_negative_ratio": (neg / total * 100) if total > 0 else 0,
        "overall_ai_accuracy": accuracy_rate
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
