import random
import string


def generate_random_password(length=13):
    # Генерация случайного пароля длиной 8 символов
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


if __name__ == '__main__':
    pass