import os
import requests


countries = [
    "US",
    "DZ",
    "DE",
    "JP",
    "CA"
]


os.makedirs("static/flags", exist_ok=True)


for country in countries:

    url = f"https://flagcdn.com/w320/{country.lower()}.png"

    response = requests.get(url)

    if response.status_code == 200:

        with open(f"static/flags/{country}.png", "wb") as file:

            file.write(response.content)

        print(f"✅ {country}.png downloaded")

    else:

        print(f"❌ Failed {country}")