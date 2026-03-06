class Currencies():
    """
    Модель, которая хранит информацию о валюте
    """

    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: float):
        """
        :param id: id валюты
        :param code: Код валюты
        :param name: Название валюты
        :param value: Значение валюты
        :param nominal: Номинал валюты
        """
        self.id: str = id
        self.num_code: str = num_code
        self.char_code: str = char_code
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
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str):
        if type(num_code) is str:
            self.__num_code = num_code
        else:
            raise ValueError('Ошибка при задании num_code валюты')

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) is str:
            self.__char_code = char_code
        else:
            raise ValueError('Ошибка при задании char_code валюты')

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
