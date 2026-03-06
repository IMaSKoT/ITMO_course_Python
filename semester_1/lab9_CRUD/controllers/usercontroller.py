from .databasecontroller import CurrencyRatesCRUD


class UserController:
    """
    Контроллер логики для управления пользователями и их подписками
    """

    def __init__(self, db_controller: CurrencyRatesCRUD):
        """
        Инициализация контроллера

        :param db_controller: Экземпляр класса для работы с БД
        """
        self.db = db_controller

    def list_users(self) -> list[dict]:
        """
        Получает список всех пользователей

        :return: Список словарей с данными пользователей
        """
        return self.db._read_users()

    def get_user_info(self, user_id: int) -> dict | None:
        """
        Получает данные конкретного пользователя по ID

        :param user_id: ID пользователя
        :return: Словарь с данными пользователя или None
        """
        return self.db._read_user_by_id(user_id)

    def get_subscriptions(self, user_id: int) -> list[dict]:
        """
        Получает список валют, на которые подписан пользователь

        :param user_id: ID пользователя
        :return: Список словарей (валют)
        """
        return self.db._read_subscriptions_by_user(user_id)
