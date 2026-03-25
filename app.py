from flask import Flask, render_template, request
from rates import load_rates
from converters import (
    km_to_miles, miles_to_km,
    kg_to_pounds, pounds_to_kg,
    celsius_to_fahrenheit, fahrenheit_to_celsius,
    usd_to_eur, eur_to_usd,
    usd_to_rub, rub_to_usd,
)

# Flask создаёт веб-приложение. __name__ говорит Flask, где искать файлы.
app = Flask(__name__)

# Тот же MENU, что в main.py — номер → (название, функция, откуда, куда)
MENU = {
    1:  ("километры → мили",     km_to_miles,            "км",   "миль"),
    2:  ("мили → километры",     miles_to_km,            "миль", "км"),
    3:  ("килограммы → фунты",   kg_to_pounds,           "кг",   "фунтов"),
    4:  ("фунты → килограммы",   pounds_to_kg,           "фунт", "кг"),
    5:  ("цельсии → фаренгейты", celsius_to_fahrenheit,  "°C",   "°F"),
    6:  ("фаренгейты → цельсии", fahrenheit_to_celsius,  "°F",   "°C"),
    7:  ("доллары → евро",       usd_to_eur,             "$",    "€"),
    8:  ("евро → доллары",       eur_to_usd,             "€",    "$"),
    9:  ("доллары → рубли",      usd_to_rub,             "$",    "₽"),
    10: ("рубли → доллары",      rub_to_usd,             "₽",    "$"),
}

# Загружаем курсы валют один раз при старте сервера
load_rates()


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

        # Читаем данные из формы
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
            return render_template("index.html", menu=MENU, error=error,
                                   last_choice=last_choice, last_value=last_value)

        label, func, unit_from, unit_to = MENU[last_choice]

        result_value = func(value)
        result = f"{value} {unit_from} = {result_value:.4f} {unit_to}"

    # render_template берёт файл templates/index.html и передаёт в него данные
    return render_template("index.html", menu=MENU, result=result, error=error,
                           last_choice=last_choice, last_value=last_value)


if __name__ == "__main__":
    # debug=True — при изменении кода сервер перезапускается автоматически
    app.run(debug=True)
