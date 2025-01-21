from decimal import Decimal
import requests
import logging
from payment_methods.models import Currency, PaymentMethod
from coins.models import Coin
from utility.common import calculate_profit

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


def calculate_coin_amount(money_amount, currency_code, coin_ticker, pay):
    """
    Метод для вычисления количества монет на основе введённой суммы,
    с учётом комиссии и выбранной валюты.
    """

    coin = Coin.objects.get(ticker=coin_ticker)
    currency = Currency.objects.get(code=currency_code)
    payment_method = PaymentMethod.objects.get(name=pay)

    price = coin.price(currency_code)  # Цена одной монеты в нужной валюте
    money_amount = Decimal(money_amount)  # суммарная стоимость монет

    profit = calculate_profit(money_amount=money_amount, currency=currency)  # Добавочная стоимость A.K.A прибыль
    payment_commission = payment_method.commission(currency=currency, price=money_amount)  # комиссия платёжной системы
    rate_network = coin.network_rate * currency.price_usd

    total_money_amount = money_amount - payment_commission - rate_network - profit

    # Рассчитываем количество монет
    amount_of_coins = total_money_amount / price
    return amount_of_coins.quantize(Decimal('0.00000001'))


if __name__ == '__main__':
    pass