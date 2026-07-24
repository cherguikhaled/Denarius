import pycountry


# ==========================================
# Currency Flag Generator
# ==========================================

def get_currency_flag(currency_code):

    try:

        currency = pycountry.currencies.get(alpha_3=currency_code)

        if not currency:
            return "flags/default.png"


        # Manual country corrections
        special_cases = {

    "USD": "US",
    "DZD": "DZ",
    "EUR": "EU",
    "JPY": "JP",
    "CAD": "CA",
    "GBP": "GB",
    "AUD": "AU",
    "CHF": "CH",

    "INR": "IN",
    "CNY": "CN",
    "BRL": "BR",
    "ZAR": "ZA",
    "KRW": "KR",
    "TRY": "TR",
    "SAR": "SA",
    "AED": "AE",
    "EGP": "EG",
    "MAD": "MA",
    "TND": "TN"

}


        if currency_code in special_cases:

            return f"flags/{special_cases[currency_code]}.png"



        return "flags/default.png"


    except Exception:

        return "flags/default.png"