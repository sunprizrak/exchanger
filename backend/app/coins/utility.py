from decimal import Decimal
import requests
import logging
from payment_methods.models import Currency

logger = logging.getLogger()


def price_coin_usdt(symbol):
    """Текущая цена Monero(XMR) в USD"""
    url = f"https://api.huobi.pro/market/detail/merged?symbol={symbol}usdt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            price = data["tick"]["close"]
            return Decimal(price)
        else:
            logger.debug("Error in API response:", data)
    except requests.exceptions.RequestException as error:
        logger.debug("HTTP Request failed:", error)


# Текущая цена Монеты в RUB
def price_coin_rub(coin_usdt):
    try:
        currency = Currency.objects.get(code='RUB')
    except Currency.DoesNotExist:
        logger.warning("Экземпляр валюты с кодом RUB не найден.")
    except Currency.MultipleObjectsReturned:
        logger.warning("Найдено несколько объектов валюты с кодом RUB.")
    usd_rub = currency.price_usd
    coin_rub = coin_usdt * usd_rub
    return coin_rub.quantize(Decimal('0.01'))


def price_coin_other_currencies(coin_rub, currency_code):
    try:
        currency = Currency.objects.get(code=currency_code)
    except Currency.DoesNotExist:
        logger.warning("Экземпляр валюты с кодом %s не найден.", currency_code)
    except Currency.MultipleObjectsReturned:
        logger.warning("Найдено несколько объектов валюты с кодом %s.", currency_code)

    coin_currency = coin_rub / currency.price_usd
    return coin_currency.quantize(Decimal('0.01'))


if __name__ == '__main__':
    pass