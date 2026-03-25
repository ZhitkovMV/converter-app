import unittest
import rates
from converters import (
    km_to_miles,
    miles_to_km,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    usd_to_eur,
    rub_to_usd,
)


class TestUnitConverters(unittest.TestCase):

    def test_km_to_miles(self):
        result = km_to_miles(1)
        self.assertAlmostEqual(result, 0.621371, places=4)

    def test_km_to_miles_zero(self):
        result = km_to_miles(0)
        self.assertEqual(result, 0)

    def test_miles_to_km(self):
        result = miles_to_km(1)
        self.assertAlmostEqual(result, 1.60934, places=4)

    def test_celsius_to_fahrenheit_freezing(self):
        # 0°C — точка замерзания воды, должна быть 32°F
        result = celsius_to_fahrenheit(0)
        self.assertEqual(result, 32)

    def test_celsius_to_fahrenheit_boiling(self):
        # 100°C — точка кипения воды, должна быть 212°F
        result = celsius_to_fahrenheit(100)
        self.assertEqual(result, 212)

    def test_fahrenheit_to_celsius_freezing(self):
        result = fahrenheit_to_celsius(32)
        self.assertEqual(result, 0)

    def test_fahrenheit_to_celsius_boiling(self):
        result = fahrenheit_to_celsius(212)
        self.assertEqual(result, 100)

    def test_celsius_and_fahrenheit_are_inverse(self):
        # Конвертируем туда и обратно — должны получить исходное число
        original = 37.0
        result = fahrenheit_to_celsius(celsius_to_fahrenheit(original))
        self.assertAlmostEqual(result, original, places=10)


class TestCurrencyConverters(unittest.TestCase):

    def setUp(self):
        # setUp вызывается перед каждым тестом.
        # Устанавливаем известные курсы, чтобы не зависеть от интернета.
        rates.RATES["USD_TO_EUR"] = 0.92
        rates.RATES["EUR_TO_USD"] = 1.09
        rates.RATES["USD_TO_RUB"] = 90.0
        rates.RATES["RUB_TO_USD"] = 1 / 90.0

    def test_usd_to_eur(self):
        result = usd_to_eur(100)
        self.assertAlmostEqual(result, 92.0, places=2)

    def test_usd_to_eur_zero(self):
        result = usd_to_eur(0)
        self.assertEqual(result, 0)

    def test_rub_to_usd(self):
        result = rub_to_usd(900)
        self.assertAlmostEqual(result, 10.0, places=2)


if __name__ == "__main__":
    unittest.main()
