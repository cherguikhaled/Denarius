from currency_flags import get_currency_flag


tests = [

    "USD",
    "DZD",
    "EUR",
    "JPY",
    "CAD",
    "INR",
    "CNY",
    "BRL"

]


for code in tests:

    print(
        code,
        "→",
        get_currency_flag(code)
    )