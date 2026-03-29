import json
import os
from flask import Flask, render_template, request
from rates import load_rates
from converters import (
    km_to_miles, miles_to_km,
    m_to_feet, feet_to_m,
    cm_to_inches, inches_to_cm,
    kg_to_pounds, pounds_to_kg,
    g_to_oz, oz_to_g,
    celsius_to_fahrenheit, fahrenheit_to_celsius,
    sqm_to_sqft, sqft_to_sqm,
    liters_to_gallons, gallons_to_liters,
    kmh_to_mph, mph_to_kmh,
    usd_to_eur, eur_to_usd,
    usd_to_rub, rub_to_usd,
    eur_to_rub, rub_to_eur,
)

# Flask создаёт веб-приложение. __name__ говорит Flask, где искать файлы.
app = Flask(__name__)

# Конвертации сгруппированы по категориям:
# категория → { "label": название, "conversions": { номер → (название, функция, откуда, куда) } }
CATEGORIES = {
    "length": {
        "label": "Длина",
        "conversions": {
            1:  ("километры → мили",       km_to_miles,   "км",  "миль"),
            2:  ("мили → километры",       miles_to_km,   "миль","км"),
            11: ("метры → футы",           m_to_feet,     "м",   "фут"),
            12: ("футы → метры",           feet_to_m,     "фут", "м"),
            13: ("сантиметры → дюймы",     cm_to_inches,  "см",  "дюйм"),
            14: ("дюймы → сантиметры",     inches_to_cm,  "дюйм","см"),
        },
    },
    "weight": {
        "label": "Вес",
        "conversions": {
            3:  ("килограммы → фунты",     kg_to_pounds,  "кг",  "фунтов"),
            4:  ("фунты → килограммы",     pounds_to_kg,  "фунт","кг"),
            15: ("граммы → унции",         g_to_oz,       "г",   "унц"),
            16: ("унции → граммы",         oz_to_g,       "унц", "г"),
        },
    },
    "temperature": {
        "label": "Температура",
        "conversions": {
            5:  ("цельсии → фаренгейты",   celsius_to_fahrenheit, "°C", "°F"),
            6:  ("фаренгейты → цельсии",   fahrenheit_to_celsius, "°F", "°C"),
        },
    },
    "currency": {
        "label": "Валюта",
        "conversions": {
            7:  ("доллары → евро",         usd_to_eur,    "$",  "€"),
            8:  ("евро → доллары",         eur_to_usd,    "€",  "$"),
            9:  ("доллары → рубли",        usd_to_rub,    "$",  "₽"),
            10: ("рубли → доллары",        rub_to_usd,    "₽",  "$"),
            17: ("евро → рубли",           eur_to_rub,    "€",  "₽"),
            18: ("рубли → евро",           rub_to_eur,    "₽",  "€"),
        },
    },
    "area": {
        "label": "Площадь",
        "conversions": {
            19: ("кв. метры → кв. футы",   sqm_to_sqft,   "м²",  "фут²"),
            20: ("кв. футы → кв. метры",   sqft_to_sqm,   "фут²","м²"),
        },
    },
    "volume": {
        "label": "Объём",
        "conversions": {
            21: ("литры → галлоны",        liters_to_gallons,  "л",  "гал"),
            22: ("галлоны → литры",        gallons_to_liters,  "гал","л"),
        },
    },
    "speed": {
        "label": "Скорость",
        "conversions": {
            23: ("км/ч → миль/ч",          kmh_to_mph,    "км/ч",  "mph"),
            24: ("миль/ч → км/ч",          mph_to_kmh,    "mph",   "км/ч"),
        },
    },
}

# Плоский словарь для быстрого поиска по номеру — номер → (название, функция, откуда, куда)
ALL_CONVERSIONS = {}
for category in CATEGORIES.values():
    ALL_CONVERSIONS.update(category["conversions"])

# Загружаем курсы валют один раз при старте сервера
load_rates()

HISTORY_FILE = "history.json"

# Загружаем историю из файла при старте; если файла нет — начинаем с пустого списка
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (json.JSONDecodeError, ValueError):
        history = []
else:
    history = []


# @app.route — говорит Flask: "когда пользователь открывает /,
# вызови функцию index()"
# methods=["GET", "POST"] — страница умеет принимать и открытие, и отправку формы
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    last_choice = None
    last_value = ""

    # POST — это когда пользователь нажал кнопку "Конвертировать"
    if request.method == "POST":

        # Читаем категорию и данные из формы
        selected_category = request.form.get("category", "")
        raw_choice = request.form["choice"]
        raw_value = request.form["value"]

        # Запоминаем, что ввёл пользователь — вернём обратно в шаблон
        last_choice = int(raw_choice)
        last_value = raw_value

        # Проверяем, что пользователь ввёл число
        try:
            value = float(raw_value)
        except ValueError:
            error = "Ошибка: введите число."
            return render_template("index.html", categories=CATEGORIES,
                                   selected_category=selected_category,
                                   error=error, last_choice=last_choice,
                                   last_value=last_value, history=history)

        label, func, unit_from, unit_to = ALL_CONVERSIONS[last_choice]

        result_value = func(value)
        result = f"{value} {unit_from} = {result_value:.4f} {unit_to}"

        # Добавляем запись в начало истории и обрезаем до 10 записей
        history.insert(0, {
            "label": label,
            "input": f"{value} {unit_from}",
            "output": f"{result_value:.4f} {unit_to}",
        })
        del history[10:]

        # Сохраняем обновлённую историю в файл
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    else:
        # GET — пользователь выбрал категорию (или просто открыл страницу)
        selected_category = request.args.get("category", "")

    # render_template берёт файл templates/index.html и передаёт в него данные
    return render_template("index.html", categories=CATEGORIES,
                           selected_category=selected_category,
                           result=result, error=error,
                           last_choice=last_choice, last_value=last_value,
                           history=history)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
