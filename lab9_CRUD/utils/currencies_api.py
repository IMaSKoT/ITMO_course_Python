from datetime import datetime, timedelta

import requests
import sys


def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                   handle=sys.stdout) -> dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
        url: Адрес, по которому производится запрос
        handle: Объект записи данных

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    try:

        response = requests.get(url)

        # print(response.status_code)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        # print(data)
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = (data["Valute"][code]["CharCode"],
                                        data["Valute"][code]["NumCode"],
                                        data["Valute"][code]["Name"],
                                        data["Valute"][code]["Value"],
                                        data["Valute"][code]["Nominal"])
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        # print(f"Ошибка при запросе к API: {e}", file=handle)
        handle.write(f"Ошибка при запросе к API: {e}")
        # raise ValueError('Упали с исключением')
        raise requests.exceptions.RequestException('Упали с исключением')


def get_currencies_with_days(currency_codes: list, handle=sys.stdout, days=90) -> dict:
    """
    Получает курсы валют с API Центробанка России за определенные дни.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
        handle: Объект записи данных
        days: Количество дней, за которые берется статистика

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    results = {code: [] for code in currency_codes}
    last_result = {}
    for day in range(days, -1, -1):
        target_date = datetime.now() - timedelta(days=day)
        date_str = target_date.strftime("%Y/%m/%d")
        url = f"https://www.cbr-xml-daily.ru/archive/{date_str}/daily_json.js"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if response.status_code == 404 and last_result != {}:
                for code in currency_codes:
                    results[code].append({'date': target_date.strftime("%Y-%m-%d"),
                                          'value': last_result[code]['value']})
                    continue

            if "Valute" in data:
                for code in currency_codes:
                    if code in data["Valute"]:
                        results[code].append({'date': target_date.strftime("%Y-%m-%d"),
                                              'value': data['Valute'][code]['Value']})
                        last_result[code] = {'value': data['Valute'][code]['Value'],
                                             'code': code}
                    else:
                        print('Кода нет в списке доступных кодов')
        except requests.exceptions.RequestException as e:
            handle.write(f"Ошибка при запросе к API: {e}")
            raise requests.exceptions.RequestException('Упали с исключением')
    return results
