import os
import re
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import logging

logger = logging.getLogger()


def fetch_exchange_rates():
    """ получение курсов Т-банка usd/rub покупка, byn -> rub обмен"""
    # Настройки для работы в фоновом режиме
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless")  # Фоновый режим (без интерфейса браузера)
    chrome_options.add_argument("--disable-gpu")  # Отключение GPU для совместимости
    chrome_options.add_argument("--no-sandbox")  # Полезно для работы в контейнере
    chrome_options.add_argument("--disable-dev-shm-usage")  # Устранение ограничения памяти
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Убираем флаг автоматизации
    chrome_options.add_argument("--window-size=1920,1080")  # Размер окна

    # Реалистичный user-agent
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/110.0.5481.77 Safari/537.36"
    )
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Автоматическая установка ChromeDriver
    service = Service(executable_path="/usr/bin/chromedriver")

    # Запуск Selenium WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # для действий(например навести мышь)
    actions = ActionChains(driver)

    try:
        # Открываем сайт
        driver.get("https://www.tbank.ru/about/exchange/")
        time.sleep(2)  # Ожидаем загрузку страницы

        # Получаем HTML-код
        html = driver.page_source

        # Парсинг через BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        div = soup.find("div", string=re.compile("Доллар\\(USD\\)"))
        parent_div = div.parent

        # Находим все дочерние элементы внутри родителя
        children = parent_div.find_all()

        # Получаем курс usd/rub (текст 3-го элемента (индексация с 0))
        if len(children) >= 3:
            usd_rub = children[2].get_text(strip=True).replace(',', '.')
        else:
            logger.warning("Третий элемент usd/rub не найден.")

        select = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-qa-type='uikit/select']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", select)  # Прокрутить к элементу
        open_button = select.find_element(By.CSS_SELECTOR, "span[role='button']")
        actions.move_to_element(open_button).perform()
        open_button.click()

        # Ожидание видимости выпадающего меню
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa-type='uikit/popover.popoverBlock']"))
        )
        # Находим элемент "Белорусский рубль"
        element = dropdown.find_element(By.XPATH, ".//*[text()='Белорусский рубль']")
        element.click()

        time.sleep(5)

        # Получаем HTML-код
        html = driver.page_source

        # Парсинг через BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Находим нужный div по классу
        div = soup.find("div", class_="bSjF5d", string="Для всех")

        parent_div = div.parent.parent

        children = parent_div.find_all()

        # Получаем курс usd/rub (текст 3-го элемента (индексация с 0))
        if len(children) >= 6:
            byn_rub = children[3].get_text(strip=True).replace(',', '.')
        else:
            logger.warning("Третий элемент usd/rub не найден.")

        usd_rub = Decimal(usd_rub).quantize(Decimal('0.01'))
        byn_rub = Decimal(byn_rub).quantize(Decimal('0.01'))

        if usd_rub and byn_rub:
            return usd_rub, byn_rub

    finally:
        # Закрываем браузер
        driver.quit()


# Пример вызова функции
if __name__ == "__main__":
    print(fetch_exchange_rates())
