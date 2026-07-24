from currency_flags import get_currency_flag


tests = [

    "USD",
    "DZD",
    "EUR",
    "JPY",
    "CAD",
    "GBP",
    "AUD",
    "CHF",
    "INR",
    "CNY",
    "BRL",
    "ZAR",
    "KRW",
    "TRY",
    "SAR",
    "AED",
    "EGP",
    "MAD",
    "TND"

]


for code in tests:

    print(
        code,
        "→",
        get_currency_flag(code)
    )