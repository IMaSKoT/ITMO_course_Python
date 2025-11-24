import math
import logging
import requests
import sys
import io
import functools


# 1 задание: Реализация декоратора logger
def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор logger для записи информации и ошибок
    :param func: Функция,которую оборачиваем
    :return: Вызываем оборачиваемую функцию
    """
    if func is None:
        return lambda func: logger(func, handle=handle)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Запись начала работа функции
        func_start = f"Запуск функции {func.__name__} с аргументами {args} {kwargs}"
        if isinstance(handle, logging.Logger):
            handle.info(func_start)
        else:
            handle.write(f"INFO: {func_start}\n")
        try:
            result = func(*args, **kwargs)
            # Запись успешного окончания работа функции
            func_end = f"Функция {func.__name__} успешно завершена. Результат: {result}"
            if isinstance(handle, logging.Logger):
                handle.info(func_end)
            else:
                handle.write(f"INFO: {func_end}\n")
            return result
        except Exception as e:
            # Запись неуспешного окончания работы функции
            func_error = f"Ошибка в функции {func.__name__}: {type(e).__name__} {e}"
            if isinstance(handle, logging.Logger):
                handle.error(func_error)
            else:
                handle.write(f"ERROR: {func_error}\n")
            raise e

    return wrapper


# 2 и 3 задание: Реализация функции get_currencies и обертка декоратором
@logger(handle=sys.stdout)
def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют с API Центробанка России.
    :param currency_codes: Список символьных кодов валют (например, ['USD', 'EUR'])
    :return: dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
                   Возвращает None в случае ошибки запроса.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    raise KeyError(f"Код валюты '{code}' не найден.")
        else:
            raise KeyError("В ответе API нет ключа 'Valute'")

        return currencies
    except requests.exceptions.ConnectionError:
        raise ConnectionError("API недоступен")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка сети: {e}")

    except ValueError:
        raise ValueError("Пришел некорректный JSON")


# Задание 4: Реализация файл-логирования
# Создаем переменную file_logger
file_logger = logging.getLogger("currency_file")
# Настраиваем на обычную запись
file_logger.setLevel(logging.INFO)
# Настраиваем место,куда будем записывать
file_handler = logging.FileHandler("currencies.log", mode='w', encoding='utf-8')
# Настраиваем форматирование, чтобы добавить WARNING и CRITICAL
formatter = logging.Formatter('%(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

file_logger.addHandler(file_handler)


# Тестируем наш file_logger используя функцию get_currencies
@logger(handle=file_logger)
def get_currencies_to_file(currency_codes):
    return get_currencies.__wrapped__(currency_codes)


try:
    get_currencies_to_file(['USD', 'EUR'])
except Exception as e:
    pass
# Задание 5: Реализуем демонстрационный пример

# Создадим отдельный math_logger для будущей функции
math_logger = logging.getLogger("quadratic.log")
math_logger.setLevel(logging.DEBUG)
math_handler = logging.FileHandler("quadratic.log", mode='w', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s: %(message)s')
math_handler.setFormatter(formatter)
math_logger.addHandler(math_handler)


# Сама функция
@logger(handle=math_logger)
def solve_quadratic(a, b, c):
    math_logger.info(f"Solving equation: {a}x^2 + {b}x + {c} = 0")

    # Ошибка типов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            math_logger.critical(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Coefficient '{name}' must be numeric")

    # Ошибка: a == 0
    if a == 0:
        math_logger.error("Coefficient 'a' cannot be zero")
        raise ValueError("a cannot be zero")

    d = b * b - 4 * a * c
    math_logger.debug(f"Discriminant: {d}")

    if d < 0:
        math_logger.warning("Discriminant < 0: no real roots")
        return None

    if d == 0:
        x = -b / (2 * a)
        math_logger.info("One real root")
        return (x,)

    root1 = (-b + math.sqrt(d)) / (2 * a)
    root2 = (-b - math.sqrt(d)) / (2 * a)
    math_logger.info("Two real roots computed")
    return root1, root2


# Тестирование этой функции


# INFO
try:
    solve_quadratic(1, -3, 2)
except:
    pass

# WARNING
try:
    solve_quadratic(1, 1, 10)
except:
    pass

# CRITICAL
try:
    solve_quadratic("строка", 1, 1)
except Exception as e:
    pass

# ERROR
try:
    solve_quadratic(0, 5, 1)
except Exception as e:
    pass
