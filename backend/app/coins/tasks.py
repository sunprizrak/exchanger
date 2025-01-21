from celery import shared_task, chain
from celery.utils.log import get_task_logger
from payment_methods.tasks import update_currencies_price
from .models import Coin
from utility.coins import (
    price_coin_usdt,
    price_coin_rub,
    price_coin_other_currencies,
)


logger = get_task_logger(__name__)


@shared_task
def update_coins_price(*args):
    coins = Coin.objects.all()

    if coins.exists():

        for coin in coins:
            symbol = coin.ticker.lower()

            coin_usdt = price_coin_usdt(symbol=symbol)
            coin_rub = price_coin_rub(coin_usdt=coin_usdt)
            coin_byn = price_coin_other_currencies(coin_rub=coin_rub, currency_code='BYN')

            logger.info(f"{coin.ticker}: {coin_usdt} USD, {coin_rub} RUB")

            coin.price_usd = coin_usdt
            coin.price_rub = coin_rub
            coin.price_byn = coin_byn
            coin.save()

    else:
        logger.warning("<<<Нет монет для получения курса!>>>")


@shared_task
def update_currencies_and_coins_price():
    chain(update_currencies_price.s(), update_coins_price.s())()