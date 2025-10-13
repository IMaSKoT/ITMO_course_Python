import timeit
import matplotlib.pyplot as plt


def build_tree_iterative(height=4, root=17, l_b=lambda x: (x - 4) ** 2, r_b=lambda y: (y + 3) * 2):
    """
    Построение бинарногодерева на основе введенных высоты, корня и правил вычисления веток
    Нерекурсивный способ
    :param height: Значение высоты дерева
    :param root: Значение корня дерева
    :param l_b: Функция, вычисляющая левую ветку
    :param r_b: Функция, вычисляющая правую ветку
    :return: Бинарное дерево
    """
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


def build_tree_recursive(height=4, root=17, l_b=lambda x: (x - 4) ** 2, r_b=lambda y: (y + 3) * 2):
    """
    Построение дерева на основе введенных высоты, корня и правил вычисления веток
    :param height: Значение высоты дерева
    :param root: Значение корня дерева
    :param l_b: Функция, вычисляющая левую ветку
    :param r_b: Функция, вычисляющая правую ветку
    :return: Бинарное дерево
    """
    # Реализация построения бинарного дерева с помощью рекурсии
    # Постепенное уменьшение высоты, пока значение height не будет равно нулю
    left_branch, right_branch = l_b(root), r_b(root)
    if height <= 0:
        return {f'{root}': []}
    else:
        return {
            f'{root}': [build_tree_recursive(height - 1, left_branch), build_tree_recursive(height - 1, right_branch)]}


def benchmark(func, number=1, repeat=5):
    """Возвращает среднее время выполнения func"""
    times = timeit.repeat(func, number=number, repeat=repeat)
    return min(times)


def main():
    """
    Запуск кода и построение графика
    """
    test_data = list(range(0, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
        res_recursive.append(benchmark(lambda: build_tree_recursive(height=n), repeat=5, number=1000))
        res_iterative.append(benchmark(lambda: build_tree_iterative(height=n), repeat=5, number=1000))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного бинарного дерева")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
