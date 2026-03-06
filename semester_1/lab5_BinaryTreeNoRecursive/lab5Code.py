import types

def gen_bin_tree(height=4, root=17, l_b=lambda x: (x - 4) ** 2, r_b=lambda y: (y + 3) * 2):
    """
        Построение бинарногодерева на основе введенных высоты, корня и правил вычисления веток
        Нерекурсивный способ
        :param height: Значение высоты дерева
        :param root: Значение корня дерева
        :param l_b: Функция, вычисляющая левую ветку
        :param r_b: Функция, вычисляющая правую ветку
        :return: Бинарное дерево; если же данные введены неправильно, то None
        """
    if isinstance(height, int) and isinstance(root, int) and isinstance(l_b, types.FunctionType) and isinstance(
            r_b, types.FunctionType):
        Tree = {f'{root}': []}
        # Создаем список, куда будем складывать элементы ветки
        a = [root]
        # Проходимся циклом, перебирая значения height и создаем новые ветки
        # за счет уже существующих
        if height <= 0:
            return Tree
        else:
            for i in range(1, height + 1):
                for j in range(2 ** (i - 1) - 1, len(a)):
                    a.append(l_b(a[j]))
                    a.append(r_b(a[j]))
        # Преобразуем все элементы в отдельные словари и в отдельном списке сохраняем ключи
        branch_for_Tree = [{f'{x}': []} for x in a]
        key_branch = [list(x.keys())[0] for x in branch_for_Tree]

        # реализуем алгоритм присоединения веток к соответствующим элементам
        # Начинаем с конца списка, объединяя по 2 элемента в один список и присоединяя его
        # к соответсвующему корню, который находится ближе к началу списка.
        # Так делаем пока не остается один элемент
        for i in range(height, 0, -1):
            k = 0
            for j in range(2 ** i - 1, len(branch_for_Tree) - 1, 2):
                new_sp = [branch_for_Tree[j], branch_for_Tree[j + 1]]
                branch_for_Tree[2 ** (i - 1) - 1 + k][key_branch[2 ** (i - 1) - 1 + k]] = new_sp
                k += 1
            branch_for_Tree = branch_for_Tree[:2 ** i - 1]
        # Возвращаем сам словарь
        return branch_for_Tree[0]
    return


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


main()
