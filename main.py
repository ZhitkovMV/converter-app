from rates import load_rates
from converters import (
    km_to_miles, miles_to_km,
    kg_to_pounds, pounds_to_kg,
    celsius_to_fahrenheit, fahrenheit_to_celsius,
    usd_to_eur, eur_to_usd,
    usd_to_rub, rub_to_usd,
)

# --- Меню: номер → (название, функция, единица откуда, единица куда) ---

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


# --- Вспомогательная функция ввода ---
# Возвращает число, или None если пользователь ввёл "back"

def get_number(prompt):
    while True:
        text = input(prompt)

        if text.strip().lower() == "back":
            return None

        try:
            return float(text)
        except ValueError:
            print("Ошибка: введите число или 'back' для возврата в меню.")


def show_menu():
    print("\n=== Конвертер единиц ===")
    for num, (label, *_) in MENU.items():
        print(f"  {num:>2}. {label}")
    print("   0. Выход")


def main():
    load_rates()

    while True:
        show_menu()

        try:
            choice = int(input("\nВыберите тип конвертации (0–10): "))
        except ValueError:
            print("Ошибка: введите целое число от 0 до 10.")
            continue

        if choice == 0:
            print("До свидания!")
            break

        if choice not in MENU:
            print("Ошибка: такого пункта нет. Введите число от 0 до 10.")
            continue

        item = MENU[choice]
        func = item[1]
        unit_from = item[2]
        unit_to = item[3]

        while True:
            value = get_number(f"\nВведите значение в {unit_from} (или 'back' для выхода в меню): ")

            if value is None:
                break

            result = func(value)
            print(f"Результат: {value} {unit_from} = {result:.4f} {unit_to}")


if __name__ == "__main__":
    main()
