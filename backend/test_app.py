import time
import requests
import json
import sys

def test_api():
    print("Testing API health check...")
    for _ in range(10):
        try:
            res = requests.get("http://localhost:8000/")
            if res.status_code == 200:
                print("API is UP.")
                break
        except requests.exceptions.ConnectionError:
            print("Waiting for API to start...")
            time.sleep(5)
    else:
        print("API failed to start within 50 seconds.")
        sys.exit(1)
        
    print("\nWaiting 30 seconds for the initial news seeding thread to complete...")
    time.sleep(30)
    
    print("\nTesting /api/signals...")
    try:
        res = requests.get("http://localhost:8000/api/signals?min_confidence=0.0")
        if res.status_code != 200:
            print(f"Failed to fetch signals. Status: {res.status_code}")
            sys.exit(1)
            
        data = res.json()
        print(f"Successfully retrieved {len(data)} signals.")
        if len(data) == 0:
            print("WARNING: No signals returned. Seeding might have failed or RSS feeds are empty.")
            sys.exit(1)
            
        # Verify structure
        first = data[0]
        required_keys = ["id", "company_name", "raw_headline", "sentiment_label", "simulated_return_impact"]
        missing = [k for k in required_keys if k not in first]
        if missing:
            print(f"Error: Missing keys in signal response: {missing}")
            sys.exit(1)
            
        print("Signal structure verified.")
        print(f"Sample Signal: {first['company_name']} | {first['sentiment_label']} | {first['industry']}")
        
    except Exception as e:
        print(f"Exception during /api/signals test: {e}")
        sys.exit(1)
        
    print("\nTesting /api/kpis...")
    try:
        res = requests.get("http://localhost:8000/api/kpis")
        if res.status_code != 200:
            print(f"Failed to fetch KPIs. Status: {res.status_code}")
            sys.exit(1)
            
        kpis = res.json()
        print(f"Successfully retrieved KPIs: {json.dumps(kpis, indent=2)}")
        if kpis['total_active_alerts'] == 0:
            print("Error: KPIs show 0 active alerts, but signals endpoint returned data.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Exception during /api/kpis test: {e}")
        sys.exit(1)
        
    print("\n--- ALL TESTS PASSED SUCCESSFULLY ---")
    
if __name__ == "__main__":
    test_api()
