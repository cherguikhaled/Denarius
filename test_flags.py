import pycountry


currencies = [
    "USD",
    "DZD",
    "EUR",
    "JPY",
    "CAD"
]


for currency in currencies:

    result = pycountry.currencies.get(alpha_3=currency)

    if result:

        print(currency, "→", result.name)

    else:

        print(currency, "→ Not found")