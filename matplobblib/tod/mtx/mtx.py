from ...forall import *

MTX = []

def mtx1(a, b, c):
    '''
    Задайте одномерный массив аг1 размерности, состоящий из {a} случайных целых чисел в пределах от {b} до {c}. Получите массив индексов, отсортированных по убыванию элементов массива. Выведите на печать массив ar1 с отсортированными элементами. Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.
    Args: a,b,c
    '''
    import numpy as np


    ar1 = np.random.randint(a, b, c)


    sorted_indices = np.argsort(-ar1)


    sorted_ar1 = ar1[sorted_indices]


    print("Исходный массив:", ar1)
    print("Индексы по убыванию:", sorted_indices)
    print("Отсортированный массив:", sorted_ar1)

def mtx2(a,b,c,d):
    '''Создать матрицу {a} на {b} из случайных целых (используя модуль 'numpy.random) чисел из диапозона от {c} до {d} и найти в ней строку (ее индекс и вывести саму, строку), в которой сумма значений минимальна.'''
    matrix = np.random.randint(c, d, size=(a, b))


    row_sums = np.sum(matrix, axis=1)


    min_row_index = np.argmin(row_sums)

    min_row = matrix[min_row_index]


    print("Матрица 8x10:")
    print(matrix)
    print("Индекс:",min_row_index)
    print("Сама строка", min_row)


def mtx3():
    ''' Без непосредственного задания элементов матрицы создать в питру матрицу 11 на 6 вида: [[1, 2, 4, 7, 8, 9], [11, 12, 14, 17, 18, 19], (21, 22, 24, 27, 28, 29], ..., [101, 102, 104, 107, 108, 109]]'''
    start_values = np.arange(1, 102, 10).reshape(-1, 1)

    matrix = start_values + np.array([0, 1, 3, 6, 7, 8])

    print("Матрица 11×6:")
    print(matrix)

def mtx4():
    '''Решить матричное уравнение "A*X*B--С - найти матрицу Х. Где 'A - [[-1, 2, 4], [-3, 1, 2], 1-3, 0, 1]], В-[[3, -1], [2, 1]]`, `С-[[7, 21], [11, 8], [8, 4]].'''
    A = np.array([[-1, 2],
                [4, -3]])
    B = np.array([[1, 0],
                [0, 1]])
    C = np.array([[2, 3],
                [0, 1]])


    try:
        A_inv = np.linalg.inv(A)
        B_inv = np.linalg.inv(B)
    except np.linalg.LinAlgError:
        print("Одна из матриц A или B вырождена (не имеет обратной матрицы)")
    else:
        X = A_inv @ C @ B_inv
        print("Матрица X:")
        print(X)

def mtx5(a,b,c,d):
    '''Задать два двумерных массива аг1 и аг2 размерности ({a},{b}), состоящих из случайных целых чисел в пределах от {c} до {d}. Удвоить все значения аг1, которые больше значений ar2, расположенных на аналогичных позициях, остальные значения сделать равными
0. '''
    import numpy as np


    ar1 = np.random.randint(c, d+1, size=(a, b))
    ar2 = np.random.randint(c, d+1, size=(a, b))

    result = np.where(ar1 > ar2, ar1 * 2, 0)

    print("Массив ar1:\n", ar1)
    print("Массив ar2:\n", ar2)
    print("Результат:\n", result)

def mtx6(a,b,c,d):
    '''Задайте двумерный массив аг1 размерности ({a}, {b}), состоящий из случайных целых чисел в пределах от {b} до {c}. Определите, в каких столбцах не менее 2 раз встречается значение, максимальное по своей строке и распечатайте массив с заменой элементов остальных столбцов на 1. Решить задачу средствами пumpy и/или pandas. He использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.'''
    ar1 = np.random.randint(c, d+1, size=(a, b))
    print("Исходный массив:")
    print(ar1)


    max_in_rows = np.max(ar1, axis=1, keepdims=True)


    is_max = (ar1 == max_in_rows)


    max_counts = np.sum(is_max, axis=0)


    valid_columns = max_counts >= 2


    mask = np.zeros_like(ar1, dtype=bool)
    mask[:, valid_columns] = True


    result = np.where(mask, ar1, -1)

    print("\nРезультат:")
    print(result)


def mtx7(a,b,c,d):
    '''Задайте двумерный массив аг1 размерности, состоящий из случайных целых чисел в пределах от {a} до {b} размерности ({c},{d}). Получите массив, в котором нечетные элементы заменены на -1. Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.'''
    ar1 = np.random.randint(a, b+1, size=(c, d))

    print("Исходный массив:")
    print(ar1)


    result = np.where(ar1 % 2 != 0, -1, ar1)

    print("\nМассив с заменой нечетных элементов на -1:")
    print(result)

def mtx8(a,b,c, d):
    '''Сгенерировать двухмерный массив `arr` размерности ({a}, {b}), состоящий из случайных действительных чисел, равномерно распределенных в диапазоне от {c} до {d}.
Нормализовать значения массива с помощью преобразования вида $ax+b$ так, что после нормализации максимальный элемент массива будет равен 1.0, минимальный 0.0'''
    import numpy as np

    arr = np.random.uniform(c, d, size = (a, b))
    print(arr, '\n')
    min_val = np.min(arr)
    max_val = np.max(arr)
    a = 1 / (max_val - min_val)
    b = -a * min_val
    norm_arr = a * arr + b
    print(norm_arr)

    print("\nМаксимальный элемент нормализованного массива:", np.max(norm_arr))
    print("Минимальный элемент нормализованного массива:", np.min(norm_arr))
    
MTX = [mtx1,mtx2,mtx3,mtx4,mtx5,mtx6,mtx7,mtx8]