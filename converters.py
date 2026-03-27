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


# --- Длина (расширение) ---

def m_to_feet(m):
    return m * 3.28084

def feet_to_m(ft):
    return ft / 3.28084

def cm_to_inches(cm):
    return cm / 2.54

def inches_to_cm(inches):
    return inches * 2.54


# --- Вес (расширение) ---

def g_to_oz(g):
    return g / 28.3495

def oz_to_g(oz):
    return oz * 28.3495


# --- Площадь ---

def sqm_to_sqft(sqm):
    return sqm * 10.7639

def sqft_to_sqm(sqft):
    return sqft / 10.7639


# --- Объём ---

def liters_to_gallons(liters):
    return liters * 0.264172

def gallons_to_liters(gallons):
    return gallons / 0.264172


# --- Скорость ---

def kmh_to_mph(kmh):
    return kmh * 0.621371

def mph_to_kmh(mph):
    return mph * 1.60934


# --- Функции конвертации валют: берут курс из RATES ---

def usd_to_eur(usd):
    return usd * RATES["USD_TO_EUR"]

def eur_to_usd(eur):
    return eur * RATES["EUR_TO_USD"]

def usd_to_rub(usd):
    return usd * RATES["USD_TO_RUB"]

def rub_to_usd(rub):
    return rub * RATES["RUB_TO_USD"]

def eur_to_rub(eur):
    return eur * RATES["EUR_TO_RUB"]

def rub_to_eur(rub):
    return rub * RATES["RUB_TO_EUR"]
