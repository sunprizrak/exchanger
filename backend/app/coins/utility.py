from decimal import Decimal
import requests
import logging
from payment_methods.models import Currency
from .models import Coin

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


def calculate_coin_amount(money_amount, currency_code, coin_ticker):
    """
    Метод для вычисления количества монет на основе введённой суммы,
    с учётом комиссии и выбранной валюты.
    """

    coin = Coin.objects.get(ticker=coin_ticker)
    currency = Currency.objects.get(code=currency_code)

    # Приводим amount к Decimal
    money_amount = Decimal(money_amount)
    money_amount_usd = money_amount / currency.price_usd

    # Максимальная комиссия СБП в RUB
    max_rate_sbp = Decimal(1700)

    # Получаем цену монеты в нужной валюте
    if currency_code == 'RUB' and coin.price_rub:
        price = coin.price_rub
    elif currency_code == 'BYN' and coin.price_byn:
        price = coin.price_byn
        max_rate_sbp = max_rate_sbp / currency.price_rub
    else:
        raise ValueError(f"Не найдена цена для валюты {currency_code}.")

    rate_sbp = money_amount * Decimal((0.5 / 100))

    if rate_sbp > max_rate_sbp:
        rate_sbp = max_rate_sbp

    rate_network = coin.network_rate * currency.price_usd

    def calculate_profit():
        if 10 <= money_amount_usd < 20:
            return currency.price_usd * Decimal(1.5)
        elif 20 <= money_amount_usd < 30:
            return currency.price_usd * Decimal(2)
        elif 30 <= money_amount_usd < 100:
            return currency.price_usd * Decimal(2.5)
        elif 100 <= money_amount_usd < 300:
            return currency.price_usd * Decimal(3)
        elif 300 <= money_amount_usd:
            return currency.price_usd * Decimal(4)

    profit = calculate_profit()

    total_money_amount = money_amount - rate_network - rate_sbp - profit

    # Рассчитываем количество монет
    amount_of_coins = total_money_amount / price
    return amount_of_coins.quantize(Decimal('0.00000001'))


if __name__ == '__main__':
    pass