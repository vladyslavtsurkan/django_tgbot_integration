from decimal import Decimal

import requests
import phonenumbers


def is_valid_phone_number(phone_number: str) -> bool:
    try:
        phone_number = phonenumbers.parse(phone_number)
        return phonenumbers.is_valid_number(phone_number)
    except phonenumbers.NumberParseException:
        return False


class AlternativeClientAPITicker:
    def __init__(self, ticker):
        self.ticker = ticker

    @property
    def id(self) -> str:
        return self.ticker.get("id", "N/A")

    @property
    def name(self) -> str:
        return self.ticker.get("name", "N/A")

    @property
    def symbol(self) -> str:
        return self.ticker.get("symbol", "N/A")

    @property
    def price(self) -> Decimal:
        return Decimal(self.ticker.get("price_usd", "0"))


class AlternativeClientAPI:
    def __init__(self):
        self.base_url = "https://api.alternative.me/v1"

    def _get_ticker(self, crypto_currency_id: str):
        url = f"{self.base_url}/ticker/{crypto_currency_id}/"
        response = requests.get(url)
        return response.json()[0]

    def get_btc_ticker(self):
        return self._get_ticker("bitcoin")

    def get_eth_ticker(self):
        return self._get_ticker("ethereum")

    def get_bnb_ticker(self):
        return self._get_ticker("binancecoin")


class CalculatorRates:
    def __init__(self, ticker: AlternativeClientAPITicker):
        self.ticker = ticker

    def calculate_to_crypto(self, amount: Decimal) -> Decimal:
        return amount / self.ticker.price

    def calculate_from_crypto(self, amount: Decimal) -> Decimal:
        return amount * self.ticker.price
