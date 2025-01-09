import json
import random
import string
import hashlib
import hmac
from operator import itemgetter
from urllib.parse import parse_qsl


def generate_random_password(length=13):
    # Генерация случайного пароля длиной 8 символов
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def verify_telegram_data(token: str, init_data: str) -> bool:
    """Check incoming WebApp init data signature"""
    try:
        parsed_data = dict(parse_qsl(init_data))

        """Извлекает id и username из данных."""
        # Проверяем наличие ключа 'user'
        user_data_encoded = parsed_data.get("user")
        if not user_data_encoded:
            return None

        # Декодируем JSON-строку из значения ключа 'user'
        try:
            user_data = json.loads(user_data_encoded)
        except json.JSONDecodeError:
            return None

        # Извлекаем id и username
        user_id = user_data.get("id")
        username = user_data.get("username")
    except ValueError:
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    return (user_id, username) if calculated_hash == hash_ else False


if __name__ == '__main__':
    pass