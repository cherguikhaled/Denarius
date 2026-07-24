from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()


CURRENCYBEACON_API_KEY = os.getenv("CURRENCYBEACON_API_KEY")

app = Flask(__name__)

# ==========================================
# Conversion History
# ==========================================

history = []

# ==========================================
# Supported Currencies
# ==========================================

currencies = {

    "USD": {
        "name": "US Dollar",
        "flag": "flags/usa.png"
    },

    "EUR": {
        "name": "Euro",
        "flag": "flags/europe.png"
    },

    "DZD": {
        "name": "Algerian Dinar",
        "flag": "flags/algeria.png"
    },

    "GBP": {
        "name": "British Pound",
        "flag": "flags/uk.png"
    },

    "JPY": {
        "name": "Japanese Yen",
        "flag": "flags/japan.png"
    },

    "CAD": {
        "name": "Canadian Dollar",
        "flag": "flags/canada.png"
    },

    "AUD": {
        "name": "Australian Dollar",
        "flag": "flags/australia.png"
    },

    "CHF": {
        "name": "Swiss Franc",
        "flag": "flags/switzerland.png"
    }

}


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
                error=None
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

        last_update=last_update,

        error=error

    )


if __name__ == "__main__":

    app.run(debug=True)
