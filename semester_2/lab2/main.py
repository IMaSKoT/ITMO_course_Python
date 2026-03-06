import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union


# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================

def create_vector() -> np.ndarray:
    """
    Создать массив от 0 до 9
    Returns:
        np.ndarray: Массив чисел от 0 до 9
    """
    return np.arange(10)


def create_matrix() -> np.ndarray:
    """
    Создать матрицу 5x5 со случайными числами [0,1]
    Returns:
        np.ndarray: Матрица 5x5 со случайными значениями
    """
    return np.random.rand(5, 5)


def reshape_vector(vec: np.ndarray) -> np.ndarray:
    """
    Преобразовать (10,) -> (2,5)
    Args:
        vec (np.ndarray): Входной массив формы (10,)
    Returns:
        np.ndarray: Преобразованный массив формы (2, 5)
    """
    return vec.reshape(2, 5)


def transpose_matrix(mat: np.ndarray) -> np.ndarray:
    """
    Транспонирование матрицы
    Args:
        mat (np.ndarray): Входная матрица
    Returns:
        np.ndarray: Транспонированная матрица
    """
    return mat.T


# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================

def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Сложение векторов одинаковой длины.
    Args:
        a (np.ndarray): Первый вектор.
        b (np.ndarray): Второй вектор.
    Returns:
        np.ndarray: Результат поэлементного сложения.
    """
    return a + b


def scalar_multiply(vec: np.ndarray, scalar: Union[int, float]) -> np.ndarray:
    """
    Умножение вектора на число
    Args:
        vec (np.ndarray): Входной вектор
        scalar (Union[int, float]): Число для умножения
    Returns:
        np.ndarray: Результат умножения вектора на скаляр
    """
    return vec * scalar


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Поэлементное умножение
    Args:
        a (np.ndarray): Первый вектор/матрица
        b (np.ndarray): Второй вектор/матрица
    Returns:
        np.ndarray: Результат поэлементного умножения
    """
    return a * b


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    Скалярное произведение
    Args:
        a (np.ndarray): Первый вектор
        b (np.ndarray): Второй вектор
    Returns:
        float: Скалярное произведение векторов
    """
    return float(np.dot(a, b))


# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================

def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Умножение матриц
    Args:
        a (np.ndarray): Первая матрица
        b (np.ndarray): Вторая матрица
    Returns:
        np.ndarray: Результат умножения матриц
    """
    return a @ b


def matrix_determinant(a: np.ndarray) -> float:
    """
    Определитель матрицы
    Args:
        a (np.ndarray): Квадратная матрица
    Returns:
        float: Определитель матрицы
    """
    return float(np.linalg.det(a))


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    """
    Обратная матрица
    Args:
        a (np.ndarray): Квадратная матрица
    Returns:
        np.ndarray: Обратная матрица
    """
    return np.linalg.inv(a)


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Решить систему Ax = b
    Args:
        a (np.ndarray): Матрица коэффициентов A
        b (np.ndarray): Вектор свободных членов b
    Returns:
        np.ndarray: Решение системы x
    """
    return np.linalg.solve(a, b)


# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

def load_dataset(path: str = "data/students_scores.csv") -> np.ndarray:
    """
    Загрузить CSV и вернуть NumPy массив
    Args:
        path (str): Путь к CSV файлу
    Returns:
        np.ndarray: Загруженные данные в виде массива
    """
    return pd.read_csv(path).to_numpy()


def statistical_analysis(data: np.ndarray) -> dict:
    """
    Рассчитать основные статистические показатели массива

    Args:
        data (np.ndarray): Одномерный массив данных

    Returns:
        dict: Словарь со статистическими показателями
    """
    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "std": np.std(data),
        "min": np.min(data),
        "max": np.max(data),
        "q25": np.percentile(data, 25),
        "q75": np.percentile(data, 75)
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Min-Max нормализация данных
    Args:
        data (np.ndarray): Входной массив данных
    Returns:
        np.ndarray: Нормализованный массив данных в диапазоне [0, 1]
    """
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val == min_val:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)


# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================

def plot_histogram(data: np.ndarray) -> None:
    """
    Построить гистограмму распределения оценок по математике

    Args:
        data (np.ndarray): Данные для гистограммы
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=5, color='skyblue', edgecolor='black')

    plt.title('Распределение оценок по математике')
    plt.xlabel('Баллы')
    plt.ylabel('Количество студентов')

    plt.savefig("plots/histogram.png")
    plt.close()


def plot_heatmap(matrix: np.ndarray) -> None:
    """
    Построить тепловую карту корреляции предметов
    Args:
        matrix (np.ndarray): Матрица корреляции
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        matrix,
        annot=True,
        cmap='coolwarm',
        fmt=".2f",
        xticklabels=['Math', 'Physics', 'Informatics'],
        yticklabels=['Math', 'Physics', 'Informatics']
    )
    plt.title('Корреляция между оценками по предметам')

    plt.savefig("plots/heatmap.png")
    plt.close()


def plot_line(x: np.ndarray, y: np.ndarray) -> None:
    """
    Построить график зависимости: студент -> оценка по математике

    Args:
        x (np.ndarray): Номера студентов
        y (np.ndarray): Оценки студентов
    """
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, 'o-', color='green', linewidth=2, markersize=8)

    plt.title('Оценки студентов по математике')
    plt.xlabel('Номер студента')
    plt.ylabel('Балл')

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.xticks(x)

    plt.savefig("plots/line_plot.png")
    plt.close()


if __name__ == "__main__":
    print("Запустите python3 -m pytest test.py -v для проверки лабораторной работы.")
    data = load_dataset("data/students_scores.csv")
    math_scores = data[:, 0]
    plot_histogram(math_scores)
    corr = np.corrcoef(data.T)
    plot_heatmap(corr)
