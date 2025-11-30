from jinja2 import Environment, PackageLoader, select_autoescape
from utils import get_currencies, get_currencies_with_days
from models import Currencies,Usercurrencies,Users,App,Author
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

#Получаем данные о валютах в currency_list
currency_list = ['USD', 'EUR', 'GBP']
currency_data = get_currencies(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js')
hist_data = get_currencies_with_days(currency_list,days = 90)
#Создаем словарь с элементами типа Currencies
currencies_dict = {}
for key,value_ in currency_data.items():
    currencies_dict[key] = Currencies(id = key,name = value_[2],value = value_[3],code = value_[1],nominal=float(value_[4]))

#Создаем список пользователей
users_list = [Users('Petr','1'),
              Users('Ivan','2'),
              Users('Fedor','3')]

#Создаем список связей
links_list = [
    Usercurrencies('1', '1', 'USD'),
    Usercurrencies('2', '2', 'EUR'),
    Usercurrencies('3', '3', 'GBP'),
    Usercurrencies('4','1','EUR')
]
#Задаем информацию об авторе и приложении
main_author = Author('Maksim Sedov', 'P3124')
my_app = App("Currencies_App","1.0",main_author)

#Подготавливаем список для html со связанными пользователями и валютами благодаря usercurrencies

#Создаем окружение
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Основной контроллер приложения, который отвечает за маршрутизацию http запросов
    """

    def do_GET(self):
        """
        Метод, обрабатывающий get запросы
        / - Главная страница
        /currencies - Страница со списком валют и их курсом
        /aboutapp - Страница с информацией об авторе и о приложении
        /users - Страница со списком всех пользователей
        /user?id= - Страница пользователя с указанным id
        """
        #global result
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)
        #Прописываем основную страницу
        if path == '/':
            template = env.get_template("index.html")
            html = template.render(myapp = "MyApp", navigation = [
                {'caption':'Главная','href':'/'},
                {'caption': 'Курсы валют', 'href': '/currencies'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'О приложении', 'href': '/aboutapp'}
            ])
        #Прописываем страницу с валютами
        elif path == '/currencies':
            template = env.get_template("currencies.html")
            html = template.render(currencies = currencies_dict.values())
        #Прописываем страницу с информацией о приложении
        elif path == '/aboutapp':
            template = env.get_template("AboutApp.html")
            html = template.render(author_name = my_app.author.name,group = my_app.author.group,AppName = my_app.name,AppVersion = my_app.version)
        #Прописываем страницу с информацией о пользователях
        elif path == '/users':
            template = env.get_template("users.html")
            html = template.render(users = users_list)
        #Прописываем информацию о каждом пользователе отдельно
        elif path == '/user':
            user_id_list = query.get('id')
            user_found = None
            user_subs = []
            user_historical_data={}
            if user_id_list:
                user_id = user_id_list[0]
                for us in users_list:
                    if us.id == user_id:
                        user_found = us
                        break
                if user_found:
                    for link in links_list:
                        if link.user_id == user_found.id:
                            curr = currencies_dict.get(link.currency_id)
                            currency_history = hist_data.get(link.currency_id)
                            if curr:
                                user_subs.append(curr)
                            if currency_history:
                                user_historical_data[link.currency_id] = currency_history

            template = env.get_template('user.html')
            html = template.render(user = user_found, user_currencies = user_subs,historical_data = user_historical_data)



        #Иначе выкидываем "Страница не найдена"
        else:
            self.send_response(404)
            self.wfile.write(b"404 Not Found")
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(html, "utf-8"))

#Запуск программы
if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()
