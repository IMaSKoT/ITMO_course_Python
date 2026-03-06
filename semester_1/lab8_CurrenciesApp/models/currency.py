class Currencies():
    """
    Модель, которая хранит информацию о валюте
    """
    def __init__(self, id:str, code:str, name:str, value: float, nominal:float):
        """
        :param id: id валюты
        :param code: Код валюты
        :param name: Название валюты
        :param value: Значение валюты
        :param nominal: Номинал валюты
        """
        self.id: str = id
        self.code: str = code
        self.name: str = name
        self.value: float = value
        self.nominal: float = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id валюты')

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code: str):
        if type(code) is str:
            self.__code = code
        else:
            raise ValueError('Ошибка при задании кода валюты')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия валюты')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if type(value) is float:
            self.__value = value
        else:
            raise ValueError('Ошибка при задании value')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: float):
        if type(nominal) is float:
            self.__nominal = nominal
        else:
            raise ValueError('Ошибка при задании номинала валюты')

