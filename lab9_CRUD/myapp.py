import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import get_currencies, get_currencies_with_days
from models import Currencies, Users, App, Author
from controllers import CurrencyRatesCRUD,UserController,CurrencyController

# Настройка Jinja2
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

# Получение исходных данных и метаинформация
currency_list = ['USD', 'EUR', 'GBP']
# Полуение данных за последний день
currency_data = get_currencies(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js', handle=sys.stdout)
# Получение данных за несколько дней
hist_data = get_currencies_with_days(currency_list, days=3, handle=sys.stdout)

main_author = Author('Maksim Sedov', 'P3124')
my_app = App("Currencies_App", "1.0", main_author)

# Инициализация БД
db_controller = CurrencyRatesCRUD()

# Заполняем валюты
currency_objects = []
for code, (_, num_code, name, value, nominal) in currency_data.items():
    cur_obj = Currencies(id="None", num_code=num_code, char_code=code, name=name, value=value, nominal=float(nominal))
    currency_objects.append(cur_obj)

currencies_to_db = []
for cur in currency_objects:
    currencies_to_db.append({
        'num_code': cur.num_code, 'char_code': cur.char_code,
        'name': cur.name, 'value': cur.value, 'nominal': cur.nominal
    })
db_controller._create_currencies(currencies_to_db)

# Заполняем пользователей
users_list = [Users('Petr', 'None'), Users('Ivan', 'None'), Users('Fedor', 'None')]
users_to_db = [{'name': user.name} for user in users_list]
db_controller._create_users(users_to_db)

# Создаем подписки
# Получаем реальные ID, которые присвоила база данных
db_users = db_controller._read_users()
db_currencies = db_controller._read_currencies()

user_name_to_id = {user['name']: user['id'] for user in db_users}
currency_code_to_id = {cur['char_code']: cur['id'] for cur in db_currencies}

# Создаем связи
links_list = [
    ('Petr', 'USD'),
    ('Ivan', 'EUR'),
    ('Fedor', 'GBP'),
    ('Petr', 'EUR')
]

subscriptions_to_db = []
for u_name, c_code in links_list:
    user_db_id = user_name_to_id.get(u_name)
    currency_db_id = currency_code_to_id.get(c_code)
    if user_db_id and currency_db_id:
        subscriptions_to_db.append({'user_id': user_db_id, 'currency_id': currency_db_id})

db_controller._create_subscription(subscriptions_to_db)

# Инициализация контроллеров логики
currency_controller = CurrencyController(db_controller)
user_controller = UserController(db_controller)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Основной контроллер приложения, который отвечает за маршрутизацию http запросов
    """

    def do_GET(self):
        """
        Метод, обрабатывающий get запросы
        Основные маршруты:
        - / : Главная страница
        - /users : Список пользователей
        - /user?id=... : Детальная страница пользователя
        - /currencies : Список валют
        - /aboutapp : Информация о приложении
        - /currency/update : Обновление курса
        - /currency/delete : Удаление валюты
        """
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        # Переменные для обработки UPDATE/DELETE
        success = False
        message = ""
        action_performed = False

        # Обработка удаления и обновления
        if path == '/currency/delete':
            action_performed = True
            char_code_list = query.get('id')  # Ожидаем char_code (например, 'USD')
            if char_code_list:
                char_code = char_code_list[0]
                try:
                    success = currency_controller.delete_currency(char_code)
                    if success:
                        message = f"Валюта {char_code} успешно удалена."
                    else:
                        message = f"Валюта {char_code} не найдена."
                except Exception:
                    message = "Ошибка: Не удалось удалить валюту."
            else:
                message = "Не указан код валюты для удаления."

        elif path == '/currency/update':
            action_performed = True
            char_code_list = query.get('id')
            new_value_list = query.get('value')

            if char_code_list and new_value_list:
                char_code = char_code_list[0]
                new_value_str = new_value_list[0]
                try:
                    new_value_float = float(new_value_str)
                    if new_value_float > 0:
                        success = currency_controller.update_currency(char_code, new_value_float)
                        if success:
                            message = f"Курс {char_code} успешно обновлен до {new_value_float}."
                        else:
                            message = f"Валюта {char_code} не найдена."
                    else:
                        message = "Новый курс должен быть положительным."
                except ValueError:
                    message = "Курс должен быть числом."
            else:
                message = "Некорректные параметры для обновления курса (нужны id и value)."

        # Редирект после действия
        if action_performed:
            status_str = "success" if success else "fail"
            encoded_message = quote(message)
            self.send_response(302)
            self.send_header('Location', f'/action_result?status={status_str}&message={encoded_message}')
            self.end_headers()
            return

        # Главная страница
        if path == '/':
            template = env.get_template("index.html")
            html = template.render(myapp="Currencies App", navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Курсы валют', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Об авторе', 'href': '/aboutapp'}
            ], )

        # О программе
        elif path == '/aboutapp':
            template = env.get_template("AboutApp.html")
            html = template.render(author_name=my_app.author.name, group=my_app.author.group,
                                   AppName=my_app.name, AppVersion=my_app.version)

        # Список пользователей
        elif path == '/users':
            template = env.get_template("users.html")
            users_data_from_db = user_controller.list_users()
            html = template.render(users=users_data_from_db)

        # Просмотр пользователя
        elif path == '/user':
            user_id_list = query.get('id')
            user_found = None
            user_subs = []
            user_historical_data = {}
            if user_id_list:
                try:
                    user_id = int(user_id_list[0])
                except ValueError:
                    user_id = -1

                user_found = user_controller.get_user_info(user_id)
                user_subs = user_controller.get_subscriptions(user_id)

                # Получение исторических данных
                if user_found:
                    for curr in user_subs:
                        currency_code = curr.get('char_code')
                        if currency_code:
                            currency_history = hist_data.get(currency_code)
                            if currency_history:
                                user_historical_data[currency_code] = currency_history

            template = env.get_template('user.html')
            html = template.render(user=user_found, user_currencies=user_subs, historical_data=user_historical_data)

        # Список валют
        elif path == '/currencies':
            template = env.get_template("currencies.html")
            currencies_data_from_db = currency_controller.list_currencies()
            html = template.render(currencies=currencies_data_from_db)

        # Debug: Вывод в консоль
        elif path == '/currency/show':
            currencies = currency_controller.list_currencies()
            print("\n--- DEBUG: ВСЕ ВАЛЮТЫ ---")
            for c in currencies:
                print(f"[{c['char_code']}]: {c['value']}")
            print("---------------------------\n")

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes("Курсы валют выведены в консоль сервера.", "utf-8"))
            return

        # 7. Страница результата действия
        elif path == '/action_result':
            status = query.get('status', ['fail'])[0]
            message = query.get('message', ['Неизвестная ошибка'])[0]
            template = env.get_template('index.html')
            html = template.render(myapp="Результат операции",
                                   navigation=[
                                       {'caption': 'Курсы валют', 'href': '/currencies'},
                                       {'caption': 'Пользователи', 'href': '/users'}
                                   ],
                                   a_variable=f"Операция завершена. Статус: {status}. Сообщение: {message}")

        # 404 Not Found
        else:
            self.send_response(404)
            self.wfile.write(b"404 Not Found")
            return

        # Отправка успешного ответа с HTML
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(html, "utf-8"))


# Запуск программы
if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running on http://localhost:8080')
    httpd.serve_forever()
