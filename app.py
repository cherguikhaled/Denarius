from flask import Flask, render_template, request
import requests

app = Flask(__name__)


currencies = {

    "USD": "🇺🇸 USD",

    "EUR": "🇪🇺 EUR",

    "DZD": "🇩🇿 DZD",

    "GBP": "🇬🇧 GBP",

    "JPY": "🇯🇵 JPY",

    "CAD": "🇨🇦 CAD",

    "AUD": "🇦🇺 AUD",

    "CHF": "🇨🇭 CHF"

}


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    rate = None
    amount = None
    from_currency = None
    to_currency = None
    error = None


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
                amount=None,
                from_currency=from_currency,
                to_currency=to_currency,
                currencies=currencies,
                error=None
            )


        try:

            amount = float(request.form["amount"])


        except ValueError:

            error = "Please enter a valid amount."
            amount = None



        if amount is not None:


            if amount <= 0:

                error = "Amount must be greater than zero."


            elif from_currency == to_currency:

                error = "Please choose two different currencies."


            else:


                url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"


                try:

                    response = requests.get(url, timeout=5)

                    data = response.json()


                    if "rates" in data:

                        rate = data["rates"][to_currency]

                        result = amount * rate


                    else:

                        error = "Unable to get exchange rate."



                except requests.exceptions.RequestException:

                    error = "Connection error. Please try again later."



                except KeyError:

                    error = "Currency not supported."



    return render_template(

        "index.html",

        result=result,

        rate=rate,

        amount=amount,

        from_currency=from_currency,

        to_currency=to_currency,

        currencies=currencies,

        error=error

    )



if __name__ == "__main__":

    app.run(debug=True)