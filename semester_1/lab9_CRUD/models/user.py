class Users():
    """
    Модель, которая хранит информацию о пользователях
    """

    def __init__(self, name: str, id: str):
        """
        :param name: Имя пользователя
        :param id: id пользователя
        """
        self.name: str = name
        self.id: str = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id пользователя')
