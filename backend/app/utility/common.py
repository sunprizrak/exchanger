from decimal import Decimal


def calculate_profit(money_amount, currency):
    money_amount_usd = money_amount / currency.price_usd

    if money_amount_usd < 300:
        return currency.price_usd * Decimal(1.5)
    elif 300 <= money_amount_usd:
        return currency.price_usd * Decimal(3)