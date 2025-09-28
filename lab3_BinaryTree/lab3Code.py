import types


def main():
    """
    Функция запуска кода
    :return: None
    """
    try:
        height = int(input("Введите высоту дерева: "))
        root = int(input("Введите значения корня: "))
        print(gen_bin_tree(height, root))
    except:
        print('Неккоректные данные или слишком большие значения')


def left_branch17(root: int) -> int:
    """
    Вычисление значения левой ветки
    :param root: Значение корня этой ветки
    :return: Вычисляет значение ветки: (root-4)**2
    """
    return (root - 4) ** 2


def right_branch17(root: int) -> int:
    """
    Вычисление значения правой ветки
    :param root: Значение корня этой ветки
    :return: Вычисляет значение ветки: (root+3)*2
    """
    return (root + 3) * 2


def gen_bin_tree(height=4, root=17, l_b=left_branch17, r_b=right_branch17):
    """
    Построение дерева на основе введенных высоты, корня и правил вычисления веток
    :param height: Значение высоты дерева
    :param root: Значение корня дерева
    :param l_b: Функция, вычисляющая левую ветку
    :param r_b: Функция, вычисляющая правую ветку
    :return: Бинарное дерево; если же данные введены неправильно, то None
    """
    # Проверка на корректно введенные данные
    if isinstance(height, int) or not isinstance(root, int) or not isinstance(l_b, types.FunctionType) or not (
            r_b, types.FunctionType):
        # Проверка на корректно введенную функцию
        try:
            left_branch, right_branch = l_b(root), r_b(root)
        except:
            return
        # Реализация построения бинарного дерева с помощью рекурсии
        # Постепенное уменьшение высоты, пока значение height не будет равно нулю
        if height <= 0:
            return {f'{root}': []}
        else:
            return {f'{root}': [gen_bin_tree(height - 1, left_branch), gen_bin_tree(height - 1, right_branch)]}
    else:
        return


main()
