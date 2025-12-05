from .databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """
    Контроллер логики для управления валютами
    Связывает маршрутизатор и базу данных
    """

    def __init__(self, db_controller: CurrencyRatesCRUD):
        """
        Инициализация контроллера

        :param db_controller: Экземпляр класса для работы с БД
        """
        self.db = db_controller

    def list_currencies(self) -> list[dict]:
        """
        Получает список всех валют

        :return: Список словарей с данными валют
        """
        return self.db._read_currencies()

    def update_currency(self, char_code: str, value: float) -> bool:
        """
        Обновляет курс валюты

        :param char_code: Буквенный код валюты (например, 'USD')
        :param value: Новое значение курса
        :return: True, если обновление прошло успешно
        """
        return self.db._update_currency_value(char_code, value)

    def delete_currency(self, char_code: str) -> bool:
        """
        Удаляет валюту по буквенному коду

        :param char_code: Буквенный код валюты (например, 'USD')
        :return: True, если удаление прошло успешно
        """
        return self.db._delete_currency(char_code)
