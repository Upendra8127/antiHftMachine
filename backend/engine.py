import json
import re
from transformers import pipeline
import yfinance as yf
import feedparser
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("spaCy model not loaded yet.")
    nlp = None

# Load NIFTY 500 mappings (Aliases) for fallback/exact matching
with open("nifty500.json", "r") as f:
    NIFTY_500 = json.load(f)

# Initialize FinBERT
print("Loading FinBERT model...")
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
print("FinBERT model loaded.")

BLACKLIST_PHRASES = [
    r"multibagger", r"guaranteed returns", r"sponsored content", r"100% accurate", r"sure shot"
]

AMBIGUOUS_GROUPS = ["adani", "tata", "bajaj", "birla", "mahindra", "godrej"]

def extract_entities(text: str):
    """V2: Dynamically extract company/ORG names and check ambiguity."""
    if not nlp: return None, None, None, False
    
    doc = nlp(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    if not orgs:
        return None, None, None, False
        
    primary_org = orgs[0]
    primary_org_lower = primary_org.lower()
    
    ticker = None
    needs_clarification = False
    industry = "General"
    
    # Check ambiguity
    for group in AMBIGUOUS_GROUPS:
        if group in primary_org_lower:
            needs_clarification = True
            
            # Simple keyword extraction for industry context
            if "power" in text.lower(): industry = "Power/Energy"
            elif "green" in text.lower() or "renew" in text.lower(): industry = "Renewable Energy"
            elif "port" in text.lower(): industry = "Ports/Logistics"
            elif "motor" in text.lower() or "auto" in text.lower(): industry = "Automotive"
            elif "steel" in text.lower(): industry = "Metals/Mining"
            elif "bank" in text.lower() or "finan" in text.lower(): industry = "Banking/Finance"
            break
            
    # Try to map to ticker if possible
    for t, aliases in NIFTY_500.items():
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', primary_org, re.IGNORECASE):
                ticker = t
                break
        if ticker: break
        
    # If it's a known ambiguous group, we still force clarification even if a partial ticker matched
    if needs_clarification:
        ticker = None # We let the user figure it out via manual clarification

    # If we couldn't find a ticker for an extracted ORG, set it to the ORG name
    if not ticker and not needs_clarification:
        ticker = primary_org[:10].upper() # Mock ticker
        
    return ticker, primary_org, industry, needs_clarification

def pre_sentiment_filter(text: str, company_name: str):
    """Returns True if the text is SPAM/MANIPULATED, False otherwise."""
    text_lower = text.lower()
    for phrase in BLACKLIST_PHRASES:
        if re.search(phrase, text_lower): return True
    if len(text_lower) == 0: return True
    company_mentions = text_lower.count(company_name.lower())
    if (company_mentions * len(company_name)) / len(text_lower) > 0.05: return True
    return False

def analyze_sentiment(text: str):
    """Run text through FinBERT and map to BUY/SELL."""
    try:
        result = sentiment_analyzer(text[:512])[0]
        label = result['label'].upper()
        score = result['score']
        
        # V2 Mapping
        if label == 'POSITIVE':
            action_label = "BUY POSITION"
            simulated_impact = score * 5.0
        elif label == 'NEGATIVE':
            action_label = "SELL POSITION"
            simulated_impact = -score * 5.0
        else:
            action_label = "HOLD"
            simulated_impact = 0.0
            
        return action_label, score, simulated_impact
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "HOLD", 0.0, 0.0

def get_current_price(ticker: str):
    if not ticker: return None
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        data = stock.history(period="1d", interval="1m")
        if not data.empty: return float(data['Close'].iloc[-1])
        return None
    except Exception as e:
        return None

def fetch_rss_news():
    rss_urls = [
        "https://www.moneycontrol.com/rss/buzzingstocks.xml",
        "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "https://www.moneycontrol.com/rss/marketreports.xml"
    ]
    articles = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                articles.append({
                    "title": entry.title,
                    "summary": entry.summary if 'summary' in entry else entry.title,
                    "link": entry.link
                })
        except Exception as e:
            pass
    return articles
