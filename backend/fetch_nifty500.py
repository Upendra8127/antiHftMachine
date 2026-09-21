import pandas as pd
import json
import re
import urllib.request
import io

def generate_nifty_500():
    print("Fetching NIFTY 500 list from NSE...")
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    
    # Use a generic User-Agent to avoid basic blocks
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            csv_data = response.read()
    except Exception as e:
        print(f"Failed to fetch CSV: {e}")
        return

    df = pd.read_csv(io.BytesIO(csv_data))
    
    nifty_dict = {}
    for index, row in df.iterrows():
        symbol = str(row['Symbol']).strip()
        company_name = str(row['Company Name']).strip()
        
        # Create aliases
        aliases = set()
        aliases.add(symbol)
        aliases.add(company_name)
        
        # Clean company name for extra aliases
        clean_name = re.sub(r'\b(Limited|Ltd|Corporation|Corp|Company|Co|Inc)\b\.?', '', company_name, flags=re.IGNORECASE).strip()
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', ' ', clean_name).strip() # remove special chars
        clean_name = re.sub(r'\s+', ' ', clean_name).strip() # collapse spaces
        
        if clean_name and len(clean_name) > 2:
            aliases.add(clean_name)
            # Add first word if it's long enough and unique (basic heuristic)
            first_word = clean_name.split()[0]
            if len(first_word) > 4:
                aliases.add(first_word)
                
        nifty_dict[symbol] = list(aliases)

    with open("nifty500.json", "w") as f:
        json.dump(nifty_dict, f, indent=2)
        
    print(f"Successfully generated nifty500.json with {len(nifty_dict)} companies.")

if __name__ == "__main__":
    generate_nifty_500()
