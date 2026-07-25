from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pycountry
from pycountry_convert import country_alpha3_to_country_alpha2
import json


load_dotenv()


CURRENCYBEACON_API_KEY = os.getenv("CURRENCYBEACON_API_KEY")

app = Flask(__name__)
# ==========================================
# Flag Generator
# ==========================================

def get_currency_flag(currency_code):

    currency_country_map = {

        "USD": "US",
        "DZD": "DZ",
        "EUR": "EU",
        "JPY": "JP",
        "CAD": "CA",
        "GBP": "GB",
        "AUD": "AU",
        "CHF": "CH"

    }


    country_code = currency_country_map.get(currency_code)


    if country_code:

        return f"flags/{country_code}.png"


    return "flags/default.png"

# ==========================================
# Conversion History
# ==========================================

history = []
# ==========================================
# Top Movers (Temporary Data)
# ==========================================

top_movers = [

    {"code": "JPY", "change": 1.82},
    {"code": "CAD", "change": 0.91},
    {"code": "GBP", "change": -1.16},
    {"code": "TRY", "change": -0.84}

]
# ==========================================
# Supported Currencies
# ==========================================

# ==========================================
# Load All Currencies
# ==========================================

import json


with open("currencies.json", "r", encoding="utf-8") as file:

    currency_data = json.load(file)



currencies = {}


for item in currency_data:

    code = item["short_code"]

    currencies[code] = {

        "name": item["name"],

        "flag": get_currency_flag(code)

    }



print(f"✅ Loaded {len(currencies)} currencies")
print(currencies["USD"])
print(currencies["DZD"])
print(currencies["INR"])
# ==========================================
# Load Currencies From JSON
# ==========================================

try:

    with open("currencies.json", "r", encoding="utf-8") as file:

        currency_data = json.load(file)


    currencies = {}
    flag_map = {

    "USD": "flags/usa.png",

    "EUR": "flags/europe.png",

    "DZD": "flags/algeria.png",

    "GBP": "flags/uk.png",

    "JPY": "flags/japan.png",

    "CAD": "flags/canada.png",

    "AUD": "flags/australia.png",

    "CHF": "flags/switzerland.png"

}


    for currency in currency_data:
        for currency in currency_data:

            code = currency["short_code"]

            currencies[code] = {

                "name": currency["name"],

                "flag": flag_map.get(code, "flags/default.png")

            }


    print(f"✅ Loaded {len(currencies)} currencies")

    
except Exception as e:

    print("❌ Failed to load currencies.json")
    print(e)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    rate = None
    amount = 100

    from_currency = "USD"
    to_currency = "EUR"

    error = None

    chart_labels = []
    chart_rates = []
    trend = None
    trend_percent = None

    if request.method == "POST":

        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]

        action = request.form.get("action")

        if action == "swap":

            from_currency, to_currency = to_currency, from_currency

            return render_template(
                "index.html",
                result=None,
                rate=None,
                amount=100,
                from_currency=from_currency,
                to_currency=to_currency,
                currencies=currencies,
                history=history,
                chart_labels=[],
                chart_rates=[],
                last_update=datetime.now().strftime("%H:%M"),
                error=None,
                top_movers=top_movers,
            )

        try:
            amount = float(request.form["amount"])

        except ValueError:

            error = "Please enter a valid amount."

        if amount <= 0:

            error = "Amount must be greater than zero."

        elif from_currency == to_currency:

            error = "Please choose two different currencies."

        else:

            try:

                # =====================================
                # Current Exchange Rate
                # CurrencyBeacon API
                # =====================================

                url = (
                    f"https://api.currencybeacon.com/v1/latest"
                    f"?api_key={CURRENCYBEACON_API_KEY}"
                    f"&base={from_currency}"
                )

                response = requests.get(url, timeout=5)

                data = response.json()

                if "rates" in data:

                    rate = data["rates"][to_currency]

                    

                    result = amount * rate

                    history.insert(0, {

                        "amount": amount,
                        "from": from_currency,
                        "to": to_currency,
                        "result": round(result, 2)

                    })

                    history[:] = history[:10]
                     # =====================================
                    # Last 7 Days Chart
                    # CurrencyBeacon Timeseries
                    # =====================================

                    end_date = datetime.today().date()
                    start_date = end_date - timedelta(days=6)

                    chart_url = (
                        f"https://api.currencybeacon.com/v1/timeseries"
                        f"?api_key={CURRENCYBEACON_API_KEY}"
                        f"&base={from_currency}"
                        f"&symbols={to_currency}"
                        f"&start_date={start_date}"
                        f"&end_date={end_date}"
                    )

                    chart_response = requests.get(chart_url, timeout=5)
                    chart_data = chart_response.json()
                    if "response" in chart_data:

                        chart_labels.clear()
                        chart_rates.clear()

                        for day, values in sorted(chart_data["response"].items()):

                            if to_currency in values:

                                chart_labels.append(day)

                                chart_rates.append(values[to_currency])
                                # =====================================
                                # Price Trend (Yesterday vs Today)
                                # =====================================

                                if len(chart_rates) >= 2:

                                    yesterday = chart_rates[-2]
                                    today = chart_rates[-1]

                                    trend = "up" if today > yesterday else "down"

                                    trend_percent = round(((today - yesterday) / yesterday) * 100, 2)
                                    print("Yesterday:", yesterday)
                                    print("Today:", today)
                                    print("Trend:", trend)
                                    print("Percent:", trend_percent)
            except requests.exceptions.RequestException:

                error = "Connection error. Please try again later."

            except KeyError:

                error = "Currency not supported."

    last_update = datetime.now().strftime("%H:%M")

    return render_template(

        "index.html",

        result=result,

        rate=rate,

        amount=amount,

        from_currency=from_currency,

        to_currency=to_currency,

        currencies=currencies,

        history=history,

        chart_labels=chart_labels,

        chart_rates=chart_rates,

        trend=trend,

        trend_percent=trend_percent,

        last_update=last_update,

        error=error,

        top_movers=top_movers

    )


if __name__ == "__main__":

    app.run(debug=True)
