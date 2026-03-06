from .author import Author


class App():
    """
    Модель, которая хранит информацию об авторе, версии и имени приложения
    """

    def __init__(self, name: str, version: str, author: Author):
        """
        :param name: Название приложения
        :param version: Версия приложения
        :param author: Информация об авторе
        """
        self.name: str = name
        self.version: str = version
        self.author: Author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if type(version) is str:
            self.__version = version
        else:
            raise ValueError('Ошибка при задании версии')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self.__author = value
        else:
            raise ValueError("Переданный объект не является классом Author")
