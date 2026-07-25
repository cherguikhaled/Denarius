import os
import json
import requests

from currency_countries import currency_countries


# ==========================================
# Load currencies
# ==========================================

with open("currencies.json", "r", encoding="utf-8") as file:

    currencies = json.load(file)



# ==========================================
# Flags folder
# ==========================================

folder = "static/flags"

os.makedirs(folder, exist_ok=True)



# ==========================================
# Download flags
# ==========================================

for currency in currencies:

    code = currency["short_code"]


    country_code = currency_countries.get(code)


    if not country_code:

        print(f"⚠️ No country for {code}")

        continue



    url = f"https://flagcdn.com/w320/{country_code.lower()}.png"


    path = os.path.join(
        folder,
        f"{country_code}.png"
    )



    try:

        response = requests.get(url)


        if response.status_code == 200:

            with open(path, "wb") as file:

                file.write(response.content)


            print(
                f"✅ {code} → {country_code}.png"
            )


        else:

            print(
                f"❌ Failed {code}"
            )


    except Exception as e:

        print(
            f"❌ Error {code}: {e}"
        )