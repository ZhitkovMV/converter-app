import requests

# Курсы валют по умолчанию (используются если API недоступен)

RATES = {
    "USD_TO_EUR": 0.92,
    "EUR_TO_USD": 1.09,
    "USD_TO_RUB": 90.5,
    "RUB_TO_USD": 1 / 90.5,
}


def load_rates():
    print("Загружаю актуальные курсы валют...")
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        data = response.json()

        if data["result"] != "success":
            print("Ошибка: API вернул неуспешный ответ. Используются встроенные курсы.")
            return

        rates = data["rates"]
        RATES["USD_TO_EUR"] = rates["EUR"]
        RATES["EUR_TO_USD"] = 1 / rates["EUR"]
        RATES["USD_TO_RUB"] = rates["RUB"]
        RATES["RUB_TO_USD"] = 1 / rates["RUB"]
        print("Курсы загружены успешно.\n")

    except requests.exceptions.ConnectionError:
        print("Ошибка: нет подключения к интернету. Используются встроенные курсы.\n")
    except requests.exceptions.Timeout:
        print("Ошибка: сервер не ответил вовремя. Используются встроенные курсы.\n")
    except Exception as e:
        print(f"Неизвестная ошибка при загрузке курсов: {e}. Используются встроенные курсы.\n")
