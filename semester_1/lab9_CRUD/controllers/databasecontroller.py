import sqlite3


class CurrencyRatesCRUD:
    """
    Класс для управления базой данных
    Реализует операции CRUD для сущностей приложения
    """

    def __init__(self):
        """
        Инициализация подключения к базе данных
        """
        self.__con = sqlite3.connect(':memory:')
        self.__createtable()
        self.__cursor = self.__con.cursor()

    def __createtable(self):
        """
        Создает схему базы данных, если таблицы еще не существуют
        Создаваемые таблицы:
        1. user - хранит информацию о пользователях
        2. currency - хранит информацию о валютах
        3. user_currency - таблица связей между пользователями и валютами
        """
        cursor = self.__con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Таблица user
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """)

        # Таблица currency
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            );
        """)

        # Таблица связей user_currency
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
        """)
        self.__con.commit()

    def _create_currencies(self, currencies_data: list[dict]):
        """
        Вставка валют в базу данных

        :param currencies_data: Список словарей с данными валют

        """
        sql = """
        INSERT INTO currency (num_code, char_code, name, value, nominal)
        VALUES (:num_code, :char_code, :name, :value, :nominal)
        """
        self.__cursor.executemany(sql, currencies_data)
        self.__con.commit()

    def _create_users(self, users_data: list[dict]):
        """
        Вставка пользователей в базу данных

        :param users_data: Список словарей с именами пользователей
        """
        sql = "INSERT INTO user(name) VALUES (:name)"
        self.__cursor.executemany(sql, users_data)
        self.__con.commit()

    def _create_subscription(self, subscriptions_data: list[dict]):
        """
        Создание связей между пользователями и валютами

        :param subscriptions_data: Список словарей с ID пользователя и ID валюты

        """
        sql = "INSERT INTO user_currency (user_id, currency_id) VALUES (:user_id, :currency_id)"
        self.__cursor.executemany(sql, subscriptions_data)
        self.__con.commit()

    def _read_users(self) -> list[dict]:
        """
        Получает список всех пользователей из базы данных

        :return: Список словарей, где каждый словарь представляет пользователя
        """
        self.__cursor.execute("SELECT id, name FROM user")
        users = []
        for row in self.__cursor.fetchall():
            users.append({'id': row[0], 'name': row[1]})
        return users

    def _read_user_by_id(self, user_id: int) -> dict | None:
        """
        Получает данные одного пользователя по его id
        :param user_id: Числовой ID пользователя
        :return: Словарь с данными пользователя или None, если пользователь не найден
        """
        sql = "SELECT id, name FROM user WHERE id = ?"
        self.__cursor.execute(sql, (user_id,))
        row = self.__cursor.fetchone()
        if row:
            return {'id': row[0], 'name': row[1]}
        return None

    def _read_currencies(self) -> list[dict]:
        """
        Получает список всех доступных валют

        :return: Список словарей с полной информацией о каждой валюте
        """
        self.__cursor.execute("SELECT id, num_code, char_code, name, value, nominal FROM currency")
        currencies = []
        for row in self.__cursor.fetchall():
            currencies.append({
                'id': row[0], 'num_code': row[1], 'char_code': row[2],
                'name': row[3], 'value': row[4], 'nominal': row[5],
            })
        return currencies

    def _read_subscriptions_by_user(self, user_id: int) -> list[dict]:
        """
        Получает список валют, на которые подписан конкретный пользователь

        :param user_id: ID пользователя
        :return: Список словарей (валют)
        """
        sql = """
            SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
            FROM user_currency uc
            JOIN currency c ON uc.currency_id = c.id
            WHERE uc.user_id = ?;
        """
        self.__cursor.execute(sql, (user_id,))
        rows = self.__cursor.fetchall()
        currencies = []
        for row in rows:
            currencies.append({
                'id': row[0], 'num_code': row[1], 'char_code': row[2],
                'name': row[3], 'value': row[4], 'nominal': row[5],
            })
        return currencies

    def _update_currency_value(self, char_code: str, new_value: float) -> bool:
        """
        Обновляет курс валюты по её буквенному коду

        :param char_code: Буквенный код валюты (например, 'USD')
        :param new_value: Новое значение курса
        :return: True, если запись была обновлена, иначе False
        """
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        self.__cursor.execute(sql, (new_value, char_code))
        self.__con.commit()
        return self.__cursor.rowcount > 0

    def _delete_currency(self, char_code: str) -> bool:
        """
        Удаляет валюту по её буквенному коду
        Сначала удаляет все связанные подписки, затем удаляет саму валюту

        :param char_code: Буквенный код валюты (например, 'USD')
        :return: True, если валюта была успешно найдена и удалена
        """
        # Находим ID валюты по коду
        self.__cursor.execute("SELECT id FROM currency WHERE char_code = ?", (char_code,))
        row = self.__cursor.fetchone()
        if not row:
            return False

        currency_db_id = row[0]

        # Удаляем подписки
        self.__cursor.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_db_id,))

        # Удаляем валюту
        self.__cursor.execute("DELETE FROM currency WHERE id = ?", (currency_db_id,))
        self.__con.commit()

        return self.__cursor.rowcount > 0

    def __del__(self):
        """
        Деструктор класса
        """
        self.__cursor = None
        self.__con.close()
