from decimal import Decimal


def calculate_profit(money_amount, currency):
    money_amount_usd = money_amount / currency.price_usd

    if money_amount_usd < 300:
        return currency.price_usd * Decimal(1.5)
    elif 300 <= money_amount_usd:
        return currency.price_usd * Decimal(3)


def payment_commission(currency, price):
    sbp_percent = Decimal(0.5)
    sbp_max_comm_money = Decimal(2000)

    percent = price * (sbp_percent / 100)

    max_comm_money = sbp_max_comm_money if currency.code == 'RUB' else sbp_max_comm_money / currency.price_rub

    if percent > max_comm_money:
        return max_comm_money.quantize(Decimal('0.01'))
    else:
        return Decimal(percent).quantize(Decimal('0.01'))