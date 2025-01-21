from decimal import Decimal
from coins.models import Coin
from payment_methods.models import Currency, PaymentMethod
from .common import calculate_profit
import logging


logger = logging.getLogger()


def calculate_currency_amount(coin_amount, currency_code, coin_ticker, pay):
    """
        Метод для вычисления стоимости монет на основе введённого количества монет,
        с учётом комиссии и выбранной валюты.
    """

    coin = Coin.objects.get(ticker=coin_ticker)
    currency = Currency.objects.get(code=currency_code)
    payment_method = PaymentMethod.objects.get(name=pay)

    coin_amount = Decimal(coin_amount)

    price = coin.price(currency_code)   # Цена одной монеты в нужной валюте
    price_all_coins = price * coin_amount  # суммарная стоимость монет

    profit = calculate_profit(money_amount=price_all_coins, currency=currency)  # Добавочная стоимость A.K.A прибыль
    payment_commission = payment_method.commission(currency=currency, price=price_all_coins)  # комиссия платёжной системы
    rate_network = coin.network_rate * currency.price_usd

    total_price = price_all_coins + payment_commission * rate_network + profit
    return total_price.quantize(Decimal('0.01'))


if __name__ == '__main__':
    pass