from pycountry_convert import country_alpha3_to_country_alpha2


countries = {

    "USD": "USA",

    "DZD": "DZA",

    "EUR": "DEU",

    "JPY": "JPN",

    "CAD": "CAN"

}


for currency, country in countries.items():

    try:

        code = country_alpha3_to_country_alpha2(country)

        print(currency, "→", country, "→", code)

    except Exception as e:

        print(currency, "ERROR", e)