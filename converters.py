from rates import RATES

# --- Функции конвертации единиц: только математика, только return ---

def km_to_miles(km):
    return km * 0.621371

def miles_to_km(miles):
    return miles * 1.60934

def kg_to_pounds(kg):
    return kg * 2.20462

def pounds_to_kg(pounds):
    return pounds / 2.20462

def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


# --- Функции конвертации валют: берут курс из RATES ---

def usd_to_eur(usd):
    return usd * RATES["USD_TO_EUR"]

def eur_to_usd(eur):
    return eur * RATES["EUR_TO_USD"]

def usd_to_rub(usd):
    return usd * RATES["USD_TO_RUB"]

def rub_to_usd(rub):
    return rub * RATES["RUB_TO_USD"]
