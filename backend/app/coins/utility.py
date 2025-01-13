import requests
import logging

logger = logging.getLogger()


def get_xmr_price():
    url = "https://api.huobi.pro/market/detail/merged?symbol=xmrusdt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            price = data["tick"]["close"]
            return price
        else:
            logger.debug("Error in API response:", data)
    except requests.exceptions.RequestException as error:
        logger.debug("HTTP Request failed:", error)


def get_usd_price():
    url = 'https://open.er-api.com/v6/latest/USD'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        usd_to_rub = data['rates']['RUB']
        return usd_to_rub + 4
    else:
        logger.debug(f"Ошибка запроса: {response.status_code}")


if __name__ == '__main__':
    # Получить цену
    current_price = get_xmr_price()
    print(f"Текущая цена Monero в USDT: {current_price}")

    buy_current_pice_usd = get_usd_price()
    print(f'Курс USD/RUB: {buy_current_pice_usd}')