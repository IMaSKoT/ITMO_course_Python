def main():
    """
    Функция запуска кода.
    Запрашивает число, левую и правую границы диапазона поиска, а также тип алгоритма поиска, после вызывает функцию guess_number


    """
    target = int(input("Введите число:"))
    left = int(input("Введите левую границу:"))
    right = int(input("Введите правую границу:"))
    type = input('Введите seq для линейного поиска и bin для бинарного:')
    diap = [x for x in range(left, right + 1)]
    guess_number(target, diap, type)


def guess_number(target, diap, type) -> list[int, int] | None:
    """
    Функция угадывания числа в массиве

    :param target: Число, которое нужно угадать
    :param diap: Диапазон, в котором происходит угадывание
    :param type: Выбор алгоритма угадывания: bin - бинарный, seq - линейный
    :return: None
    """
    if type == 'seq':
        print(seq_search(target, diap))
    elif type == 'bin':
        print(binary_search(target, diap))
    else:
        return


def seq_search(target: int, diap: list) -> tuple[int, int] | str:
    """
    Алгоритм линейного поиска числа в массиве

    :param target: Число, которое нужно угадать
    :param diap: Диапазон, в котором происходит угадывание
    :return: (Число, Количество попыток) если число есть в диапазоне, а если его нет или введенные данные неккоректны, то возвращает ошибку
    """
    if isinstance(target, int) and isinstance(diap, list):
        count = 0
        for i in range(len(diap)):
            count += 1
            if diap[i] == target:
                return (target, count)
        return 'Числа нет в указанном диапазоне'
    return 'Введите корректные данные'


def binary_search(target: int, diap: list) -> tuple[int, int] | str:
    """
        Алгоритм бинарного поиска числа в массиве

        :param target: Число, которое нужно угадать
        :param diap: Диапазон, в котором происходит угадывание
        :return: (Число, Количество попыток) если число есть в диапазоне, а если его нет или введенные данные неккоректны, то возвращает ошибку
        """
    if isinstance(target, int) and isinstance(diap, list):
        count = 0
        left = 0
        right = len(diap) - 1
        mid = left + (right - left) // 2
        while left <= mid and right >= mid:
            count += 1
            if diap[mid] == target:
                return (target, count)
            if diap[mid] < target:
                left = mid + 1
                mid = left + (right - left) // 2
            if diap[mid] > target:
                right = mid - 1
                mid = left + (right - left) // 2
        return 'Числа нет в указанном диапазоне'
    return 'Введите корректные данные'
