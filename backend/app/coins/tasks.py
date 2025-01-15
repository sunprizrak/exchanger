from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Coin
from .utility import (
    price_coin_usdt,
    price_coin_rub,
)


logger = get_task_logger(__name__)


@shared_task
def update_coins_price():
    coins = Coin.objects.all()

    if coins.exists():

        for coin in coins:
            symbol = coin.ticker.lower()

            coin_usdt = price_coin_usdt(symbol=symbol)
            coin_rub = price_coin_rub(coin_usdt=coin_usdt)

            logger.info(f"{coin.ticker}: {coin_usdt} USD, {coin_rub} RUB")

            coin.price_usd = coin_usdt
            coin.price_rub = coin_rub
            coin.save()

    else:
        logger.warning("<<<Нет монет для получения курса!>>>")
