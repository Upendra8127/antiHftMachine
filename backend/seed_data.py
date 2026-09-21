from main import fetch_and_process_news, evaluate_eod_returns

print("Seeding initial data for live testing...")
fetch_and_process_news()
evaluate_eod_returns()
print("Seed complete.")
