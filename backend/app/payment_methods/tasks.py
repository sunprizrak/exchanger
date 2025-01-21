from decimal import Decimal
from utility.update_currencies_rate import fetch_exchange_rates
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Currency


logger = get_task_logger(__name__)


@shared_task
def update_currencies_price():
    currencies = Currency.objects.all()

    if currencies.exists():
        usd_rub, byn_rub = fetch_exchange_rates()

        for currency in currencies:
            if currency.code == 'RUB':
                if isinstance(usd_rub, Decimal):
                    currency.update_exchange_rate(new_price_usd=usd_rub)
                else:
                    logger.warning('Курс USD_RUB не получен')
            elif currency.code == 'BYN':
                if isinstance(byn_rub, Decimal) and isinstance(usd_rub, Decimal):
                    usd_byn = usd_rub / byn_rub
                    currency.update_exchange_rate(new_price_usd=usd_byn, new_price_rub=byn_rub)
                else:
                    logger.warning('Курс BYN_RUB не получен')

        return True
    else:
        logger.warning("<<<Курсы валют не получены>>>")
        return "Не удалось обновить курсы валют: данные отсутствуют"