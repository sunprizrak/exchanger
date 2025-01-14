import requests
import logging

logger = logging.getLogger()


def price_usdt_rub():
    """Текущая цена USDT в RUB с добавочной стоимостью на покупку"""

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "tether",
        "vs_currencies": "rub"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        price = data['tether']['rub'] + 4
        return price
    else:
        logger.debug(f"Request Error: {response.status_code}")


def price_coin_usdt(symbol):
    """Текущая цена Monero(XMR) в USD"""
    url = f"https://api.huobi.pro/market/detail/merged?symbol={symbol}usdt"
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


# Текущая цена Monero(XMR) в RUB
def price_coin_rub(coin_usdt):
    usdt_rub = price_usdt_rub()
    coin_rub = round((coin_usdt * usdt_rub), 2)
    return coin_rub



if __name__ == '__main__':
    pass