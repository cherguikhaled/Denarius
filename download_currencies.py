from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

API_KEY = os.getenv("CURRENCYBEACON_API_KEY")
print(API_KEY)
if not API_KEY:
    print("❌ CURRENCYBEACON_API_KEY not found in .env")
    exit()

url = (
    f"https://api.currencybeacon.com/v1/currencies"
    f"?api_key={API_KEY}"
)

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "response" in data:

        with open("currencies.json", "w", encoding="utf-8") as file:
            json.dump(data["response"], file, indent=4, ensure_ascii=False)

        print("✅ currencies.json created successfully.")

    else:
        print("❌ Unexpected API response.")
        print(data)

except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")