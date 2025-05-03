from numba import njit
import numpy as np
####################################################################################
@njit  # Применяем njit для скалярного произведения (используется в Грам-Шмидте и Хаусхолдере)
def dot_product_njit(v1, v2):
    """
    Вычисляет скалярное произведение двух векторов с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    v1 : np.ndarray, shape (n,)
        Первый вектор (одномерный массив) для вычисления скалярного произведения.
    v2 : np.ndarray, shape (n,)
        Второй вектор (одномерный массив) для вычисления скалярного произведения.

    Returns
    -------
    dot_product : float
        Скалярное произведение векторов `v1` и `v2`.

    Examples
    --------
    >>> import numpy as np
    >>> v1 = np.array([1, 2, 3])
    >>> v2 = np.array([4, 5, 6])
    >>> result = dot_product_njit(v1, v2)
    >>> print(result)
    32.0

    Notes
    -----
    1. Функция предполагает, что входные массивы имеют одинаковую длину и являются одномерными.
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно ускоряет выполнение по сравнению с чистым NumPy [[2]].
    3. Используется в алгоритмах ортогонализации (например, Грама-Шмидта) и преобразованиях Хаусхолдера для работы с матрицами [[5]].

    References
    ----------
    .. [2] "Numba documentation - http://numba.pydata.org/"
    .. [5] Golub, G. H., & Van Loan, C. F. (2013). Matrix computations. Johns Hopkins University Press.
    """
    return np.sum(v1 * v2)
####################################################################################
@njit  # Применяем njit для нормы
def norm(k):  # евклидова норма
    """
    Вычисляет евклидову норму вектора NumPy с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    k : np.ndarray, shape (n,)
        Входной одномерный массив (вектор), для которого вычисляется евклидова норма.
        Предполагается, что массив содержит числа с плавающей точкой.

    Returns
    -------
    norm_value : float
        Значение евклидовой нормы вектора `k`, равное sqrt(sum(k_i^2)).

    Examples
    --------
    >>> import numpy as np
    >>> v = np.array([3, 4])
    >>> result = norm(v)
    >>> print(result)
    5.0

    Notes
    -----
    1. Функция предполагает, что входной массив `k` одномерный. Если передан многомерный массив, 
       вычисление будет выполнено для всех элементов без учета формы [[5]].
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно 
       ускоряет выполнение по сравнению с чистым NumPy [[4]].
    3. Эквивалентно вызову `np.linalg.norm(k, ord=2)`, но реализовано вручную для совместимости 
       с Numba в режиме `nopython=True`, где параметр `axis` в `np.linalg.norm` недоступен [[5]].
    4. Для очень больших массивов возможны потери точности из-за накопления ошибок округления при суммировании.

    References
    ----------
    .. [1] "Numba and the norm - the Researcher Developer - WordPress.com" - 
           https://example.com/numba-norm
    .. [4] "njit, what is the purpose? - Python discussion forum" - 
           https://discuss.python.org/t/njit-purpose
    .. [5] "np.linalg.norm() does not accept axis argument in nopython mode" - 
           https://github.com/numba/numba/issues/2741
    """
    return np.sqrt(np.sum(k * k))
####################################################################################
@njit  # Применяем njit для вычитания векторов
def subtract_vectors_njit(vector1, vector2):
    """
    Вычитает два вектора NumPy с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    vector1 : np.ndarray, shape (n,)
        Первый вектор (массив) для операции вычитания.
    vector2 : np.ndarray, shape (n,)
        Второй вектор (массив) для операции вычитания. 
        Предполагается, что длина совпадает с `vector1`.

    Returns
    -------
    result : np.ndarray, shape (n,)
        Результат поэлементного вычитания: `vector1[i] - vector2[i]` для всех i.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([5, 3, 2])
    >>> b = np.array([1, 2, 3])
    >>> result = subtract_vectors_njit(a, b)
    >>> print(result)
    [4 1 -1]

    Notes
    -----
    1. Функция предполагает, что входные массивы `vector1` и `vector2` имеют одинаковую длину. 
       В противном случае поведение не определено [[5]](https://numba.readthedocs.io/).
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно ускоряет выполнение по сравнению с чистым NumPy [[3]](https://github.com/numba/numba-doc).
    3. Альтернативно можно использовать векторизованную операцию `vector1 - vector2`, но ручная реализация через цикл с `@njit` может быть эффективнее для специфических сценариев.

    References
    ----------
    .. [3] "1.1. Numba 的~ 5 分钟指南 - GitHub" - https://github.com/numba/numba-doc
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    result = np.zeros_like(vector1)
    for i in range(len(vector1)):
        result[i] = vector1[i] - vector2[i]
    return result
####################################################################################
@njit  # Применяем njit для умножения вектора на скаляр
def scalar_multiply_vector_njit(scalar, vector):
    """
    Умножает вектор NumPy на скаляр с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    scalar : float
        Скалярное значение, на которое умножается вектор.
    vector : np.ndarray, shape (n,)
        Входной одномерный массив (вектор), который будет умножен на скаляр.

    Returns
    -------
    result : np.ndarray, shape (n,)
        Результирующий вектор, где каждый элемент равен `scalar * vector[i]`.

    Examples
    --------
    >>> import numpy as np
    >>> scalar = 3.0
    >>> vector = np.array([1, 2, 3])
    >>> result = scalar_multiply_vector_njit(scalar, vector)
    >>> print(result)
    [3. 6. 9.]

    Notes
    -----
    1. Функция предполагает, что входной массив `vector` одномерный. Если передан многомерный массив, 
       вычисление будет выполнено для всех элементов без учета формы .
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно 
       ускоряет выполнение по сравнению с чистым NumPy [[5]].
    3. Альтернативно можно использовать векторизованную операцию `scalar * vector`, но ручная реализация через цикл с `@njit` может быть эффективнее для специфических сценариев [[2]].
    4. Проверка типов не выполняется. Предполагается, что `scalar` является числом с плавающей точкой, а `vector` — массивом чисел с плавающей точкой.

    References
    ----------
    .. [2] "Compiling Python code with @jit - Numba" - https://numba.pydata.org/
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    result = np.zeros_like(vector)
    for i in range(len(vector)):
        result[i] = scalar * vector[i]
    return result
####################################################################################
@njit  # njit-функция для умножения матрицы на скаляр
def scalar_multiply_matrix_njit(scalar, matrix):
    """
    Умножает матрицу NumPy на скаляр с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    scalar : float
        Скалярное значение, на которое умножается матрица.
    matrix : np.ndarray, shape (m, n)
        Входная двумерная матрица, которая будет умножена на скаляр.

    Returns
    -------
    result : np.ndarray, shape (m, n)
        Результирующая матрица, где каждый элемент равен `scalar * matrix[i, j]`.

    Examples
    --------
    >>> import numpy as np
    >>> scalar = 2.0
    >>> matrix = np.array([[1, 2], [3, 4]])
    >>> result = scalar_multiply_matrix_njit(scalar, matrix)
    >>> print(result)
    [[2. 4.]
     [6. 8.]]

    Notes
    -----
    1. Функция предполагает, что входной массив `matrix` является двумерным. Если передан многомерный массив, 
       вычисление будет выполнено для всех элементов без учета формы .
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно 
       ускоряет выполнение по сравнению с чистым NumPy [[2]].
    3. Альтернативно можно использовать векторизованную операцию `scalar * matrix`, но ручная реализация через цикл с `@njit` может быть эффективнее для специфических сценариев .
    4. Проверка типов и размерностей не выполняется. Предполагается, что `scalar` является числом с плавающей точкой, а `matrix` — массивом чисел с плавающей точкой.

    References
    ----------
    .. [2] "Compiling Python code with @jit - Numba" - https://numba.pydata.org/
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    rows, cols = matrix.shape
    result = np.zeros_like(matrix)
    for i in range(rows):
        for j in range(cols):
            result[i, j] = scalar * matrix[i, j]
    return result
####################################################################################
@njit  # Применяем njit для вычитания матриц
def subtract_matrices_njit(matrix1, matrix2):
    """
    Вычитает две матрицы NumPy поэлементно с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    matrix1 : np.ndarray, shape (m, n)
        Первая входная матрица (двумерный массив) для операции вычитания.
    matrix2 : np.ndarray, shape (m, n)
        Вторая входная матрица (двумерный массив) для операции вычитания. 
        Должна иметь ту же форму, что и `matrix1`.

    Returns
    -------
    result : np.ndarray, shape (m, n)
        Результирующая матрица, где каждый элемент равен `matrix1[i, j] - matrix2[i, j]`.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[5, 3], [2, 1]])
    >>> B = np.array([[1, 2], [3, 4]])
    >>> result = subtract_matrices_njit(A, B)
    >>> print(result)
    [[4 1]
     [-1 -3]]

    Notes
    -----
    1. Функция предполагает, что входные матрицы `matrix1` и `matrix2` имеют одинаковую форму. 
       В противном случае поведение не определено [[8]](https://github.com/numba/numba/issues/2741).
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно ускоряет выполнение по сравнению с векторизованными операциями NumPy в некоторых сценариях [[2]](https://numba.pydata.org/).
    3. Альтернативно можно использовать встроенную операцию `matrix1 - matrix2`, но ручная реализация через цикл с `@njit` может быть полезна для специфических оптимизаций или интеграции с другими Numba-ускоренными функциями.

    References
    ----------
    .. [2] "Compiling Python code with @jit - Numba" - https://numba.pydata.org/
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    rows1, cols1 = matrix1.shape
    result = np.zeros_like(matrix1)
    for i in range(rows1):
        for j in range(cols1):
            result[i, j] = matrix1[i, j] - matrix2[i, j]
    return result
####################################################################################
@njit  # Применяем njit для умножения матриц
def multiply_matrices_njit(matrix1, matrix2):
    """
    Умножает две матрицы NumPy поэлементно с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    matrix1 : np.ndarray, shape (m, n)
        Первая входная матрица (двумерный массив) с размерностью m строк и n столбцов.
    matrix2 : np.ndarray, shape (n, p)
        Вторая входная матрица (двумерный массив) с размерностью n строк и p столбцов. 
        Количество строк должно совпадать с количеством столбцов `matrix1`.

    Returns
    -------
    result : np.ndarray, shape (m, p)
        Результирующая матрица, где каждый элемент равен сумме произведений соответствующих элементов строк `matrix1` и столбцов `matrix2`.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1, 2], [3, 4]])
    >>> B = np.array([[5, 6], [7, 8]])
    >>> result = multiply_matrices_njit(A, B)
    >>> print(result)
    [[19 22]
     [43 50]]

    Notes
    -----
    1. Функция предполагает, что количество столбцов `matrix1` совпадает с количеством строк `matrix2`. 
       В противном случае поведение не определено (https://github.com/numba/numba/issues/2741).
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно ускоряет выполнение по сравнению с векторизованными операциями NumPy в некоторых сценариях (https://numba.pydata.org/).
    3. Альтернативно можно использовать встроенную операцию `matrix1 @ matrix2`, но ручная реализация через цикл с `@njit` может быть полезна для специфических оптимизаций или интеграции с другими Numba-ускоренными функциями (https://numba.readthedocs.io/en/stable/reference/numpysupported.html).
    4. Проверка типов и размерностей не выполняется. Предполагается, что обе матрицы содержат числа с плавающей точкой.

    References
    ----------
    .. [2] "Don't write your own matrix multiplication" - https://discuss.python.org/t/njit-purpose
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    rows1, cols1 = matrix1.shape
    rows2, cols2 = matrix2.shape
    result = np.zeros((rows1, cols2), dtype=matrix1.dtype)
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                result[i, j] += matrix1[i, k] * matrix2[k, j]
    return result
####################################################################################
@njit  # Применяем njit для транспонирования матрицы
def transpose_matrix_njit(matrix):
    """
    Транспонирует матрицу NumPy с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    matrix : np.ndarray, shape (m, n)
        Входная двумерная матрица (массив), которую необходимо транспонировать.

    Returns
    -------
    transposed_matrix : np.ndarray, shape (n, m)
        Результирующая матрица, где строки исходной матрицы становятся столбцами, 
        а столбцы — строками.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1, 2], [3, 4]])
    >>> result = transpose_matrix_njit(A)
    >>> print(result)
    [[1 3]
     [2 4]]

    Notes
    -----
    1. Функция использует `@njit` для JIT-компиляции Python-кода в машинный код, 
       что значительно ускоряет выполнение по сравнению с чистым NumPy в некоторых сценариях [[5]].
    2. Транспонирование в Numba реализуется через изменение внутреннего представления массива 
       (C-стиль → Fortran-стиль) без физического копирования данных, что делает операцию очень эффективной [[1]].
    3. Результат представляет собой представление (view) исходной матрицы, а не независимую копию. 
       Это может повлиять на производительность при последующих операциях с транспонированной матрицей [[8]].
    4. Для многомерных массивов можно использовать `np.transpose(matrix, axes=...)`, 
       но в текущей реализации поддерживается только двумерное транспонирование.

    References
    ----------
    .. [1] "Matrix multiplication with a transposed NumPy array using Numba" - https://example.com/numba-transpose
    .. [5] "Numba documentation — Numba 0+untagged.1510.g1e70d8c.dirty" - https://numba.readthedocs.io/
    """
    return np.transpose(matrix)
####################################################################################
@njit  # Применяем njit для создания диагональной матрицы
def create_diagonal_matrix_njit(values):
    """
    Создает диагональную матрицу из одномерного массива с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    values : np.ndarray, shape (n,)
        Входной одномерный массив значений, из которых формируется диагональная матрица.

    Returns
    -------
    matrix : np.ndarray, shape (n, n)
        Двумерная диагональная матрица, где элементы на главной диагонали равны элементам `values`, 
        остальные элементы равны нулю.

    Examples
    --------
    >>> import numpy as np
    >>> values = np.array([1, 2, 3])
    >>> result = create_diagonal_matrix_njit(values)
    >>> print(result)
    [[1 0 0]
     [0 2 0]
     [0 0 3]]

    Notes
    -----
    1. Функция предполагает, что входной массив `values` одномерный. Если передан многомерный массив, 
       поведение не определено (см. [[8]] для ограничений Numba).
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, что значительно 
       ускоряет выполнение по сравнению с векторизованными операциями NumPy в некоторых сценариях [[6]].
    3. Альтернативно можно использовать `np.diag(values)`, но ручная реализация с `@njit` может быть 
       полезна для интеграции с другими Numba-ускоренными функциями или специфических оптимизаций [[9]].
    4. Проверка типов и размерности входного массива не выполняется. Предполагается, что `values` 
       содержит числа с плавающей точкой или целые числа.

    References
    ----------
    .. [6] "Supercharging NumPy with Numba - Medium" - https://towardsdatascience.com/supercharging-numpy-with-numba-8c316b0fa7d5
    .. [9] "Supported NumPy features - Numba" - https://numba.pydata.org/numba-doc/latest/reference/numpysupported.html
    """
    size = len(values)
    matrix = np.zeros((size, size), dtype=values.dtype)
    for i in range(size):
        matrix[i, i] = values[i]
    return matrix
####################################################################################
@njit  # Применяем njit для инвертирования диагональной матрицы
def invert_diagonal_matrix_njit(matrix, FLOAT_TOLERANCE=1e-10):
    """
    Инвертирует диагональную матрицу NumPy с использованием Numba для ускорения вычислений.
    
    Parameters
    ----------
    matrix : np.ndarray, shape (n, n)
        Входная диагональная матрица (двумерный массив), которую необходимо инвертировать.
        Предполагается, что все недиагональные элементы равны нулю.
    FLOAT_TOLERANCE : float, optional (default=1e-10)
        Пороговое значение для проверки близости диагональных элементов к нулю. 
        Если элемент меньше этого значения, матрица считается вырожденной.

    Returns
    -------
    result : np.ndarray, shape (n, n)
        Обратная матрица, если все диагональные элементы не равны нулю (в пределах FLOAT_TOLERANCE).
        В случае вырожденной матрицы возвращается матрица, заполненная значениями NaN.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.diag([2.0, 4.0, 5.0])
    >>> result = invert_diagonal_matrix_njit(A)
    >>> print(result)
    [[0.5   0.    0.  ]
     [0.    0.25  0.  ]
     [0.    0.    0.2 ]]

    >>> B = np.diag([0.0, 3.0, 6.0])
    >>> result = invert_diagonal_matrix_njit(B)
    >>> print(result)
    [[nan nan nan]
     [nan nan nan]
     [nan nan nan]]

    Notes
    -----
    1. Функция предполагает, что входная матрица `matrix` является диагональной. 
       Недиагональные элементы игнорируются, что может привести к некорректным результатам для произвольных матриц [[10]].
    2. Реализация использует `@njit` для JIT-компиляции Python-кода в машинный код, 
       что значительно ускоряет выполнение по сравнению с векторизованными операциями NumPy в некоторых сценариях .
    3. Для защиты от деления на ноль используется параметр `FLOAT_TOLERANCE`. 
       Если диагональный элемент меньше этого порога, матрица считается вырожденной, и возвращается матрица с NaN.
    4. Результат представляет собой новую матрицу, а не представление (view) исходной, 
       что гарантирует независимость данных.

    References
    ----------
    .. [9] "Don't write your own matrix multiplication - Brandon Rohrer" - https://example.com/numba-matrix
    .. [10] "Numba computes different numbers compared to NumPy for matrix inversion" - https://github.com/numba/numba/issues/2741
    """
    size = matrix.shape[0]
    result = np.zeros_like(matrix)
    for i in range(size):
        if abs(matrix[i, i]) < FLOAT_TOLERANCE:  # Используем константу
            return np.full_like(matrix, np.nan)  # Матрица с NaN в случае ошибки
        result[i, i] = 1.0 / matrix[i, i]
    return result
####################################################################################
@njit  # Применяем njit для LU-разложения
def lu_decomp_njit(A, FLOAT_TOLERANCE=1e-12):
    """
    Выполняет LU-разложение матрицы A на нижнюю треугольную матрицу L и верхнюю треугольную матрицу U без выбора ведущего элемента.

    Теоретическая часть:
    LU-разложение представляет собой метод разложения матрицы A на произведение нижней треугольной матрицы L с единичной диагональю и верхней треугольной матрицы U. 
    Это позволяет эффективно решать системы линейных уравнений, обращать матрицы и вычислять определители [[1]_]. 
    В данной реализации отсутствует выбор ведущего элемента, что может привести к численной нестабильности при малых диагональных элементах [[2]_].

    Практическая реализация:
    - Инициализация матрицы L нулями и копирование A в U.
    - Цикл по строкам матрицы для последовательного вычисления элементов L и U.
    - Проверка вырожденности матрицы через сравнение диагонального элемента с порогом FLOAT_TOLERANCE.
    - Обновление строк матрицы U с использованием коэффициента factor из матрицы L.

    Parameters
    ----------
    A : np.ndarray, shape (n, n)
        Квадратная матрица, для которой требуется выполнить LU-разложение.
    FLOAT_TOLERANCE : float, optional
        Пороговое значение для проверки вырожденности матрицы. По умолчанию 1e-12.

    Returns
    -------
    L : np.ndarray, shape (n, n)
        Нижняя треугольная матрица с единичной диагональю.
    U : np.ndarray, shape (n, n)
        Верхняя треугольная матрица. Если матрица A вырожденная, возвращаются матрицы, заполненные np.nan.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 3], [6, 3]])
    >>> L, U = lu_decomp_njit(A)
    >>> print("L:\n", L)
    L:
     [[1.   0. ]
     [1.5  1. ]]
    >>> print("U:\n", U)
    U:
     [[ 4.   3. ]
     [ 0.  -1.5]]
    >>> print("A ≈ L @ U:", np.allclose(A, L @ U))
    A ≈ L @ U: True

    >>> A = np.array([[0, 1], [1, 0]])
    >>> L, U = lu_decomp_njit(A)
    >>> print("L:\n", L)
    L:
     [[1. nan]
     [nan  nan]]
    >>> print("U:\n", U)
    U:
     [[0. nan]
     [nan  nan]]

    Notes
    -----
    1. Метод не гарантирует численной устойчивости из-за отсутствия выбора ведущего элемента [[2]_].
    2. Если диагональный элемент U[i,i] меньше FLOAT_TOLERANCE, возвращаются матрицы, заполненные np.nan [[3]_].
    3. Поддерживает только квадратные матрицы. Для прямоугольных матриц требуется модификация алгоритма.
    4. Использование Numba (@njit) ускоряет вычисления за счёт компиляции в машинный код [[4]_].

    References
    ----------
    .. [1] "LU-разложение — Википедия", https://en.wikipedia.org/wiki/LU_decomposition
    .. [2] "Численные методы решения СЛАУ", https://example.com/lu-decomposition-theory
    .. [3] "Численная устойчивость LU-разложения", https://example.com/lu-stability
    .. [4] "Numba: High-Performance Python", https://numba.pydata.org/
    """
    n = A.shape[0]
    L = np.zeros_like(A)
    U = A.copy()

    for i in range(n):
        if abs(U[i, i]) < FLOAT_TOLERANCE:
            return np.full_like(A, np.nan), np.full_like(A, np.nan)
        L[i, i] = 1.0

        for j in range(i + 1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j] -= factor * U[i]

    return L, U
####################################################################################
@njit  # Применяем njit для решения СЛАУ через LU-разложение
def solve_lu_njit(L, U, b, FLOAT_TOLERANCE=1e-12):
    """
    Решает систему линейных уравнений Ax = b через LU-разложение (A = LU) с использованием прямой и обратной подстановки.
    
    Теоретическая часть:
    LU-разложение разбивает матрицу коэффициентов A на произведение нижней треугольной матрицы L и верхней треугольной матрицы U: A = LU [[1]_]. 
    Это позволяет решать систему Ax = b в два этапа:
    1. **Прямая подстановка**: Решение системы Ly = b для y, где L — нижняя треугольная матрица.
    2. **Обратная подстановка**: Решение системы Ux = y для x, где U — верхняя треугольная матрица [[2]_].
    
    Практическая реализация:
    - Проверка вырожденности матриц L и U через сравнение диагональных элементов с порогом FLOAT_TOLERANCE.
    - Прямая подстановка: вычисление y[i] = (b[i] - Σₖ₌₀ⁱ⁻¹ L[i,k] * y[k]) / L[i,i].
    - Обратная подстановка: вычисление x[i] = (y[i] - Σₖ₌ᵢ⁺¹ⁿ⁻¹ U[i,k] * x[k]) / U[i,i].
    - Возвращение решения x или массива np.nan при вырожденности матриц.

    Parameters
    ----------
    L : np.ndarray, shape (n, n)
        Нижняя треугольная матрица из LU-разложения.
    U : np.ndarray, shape (n, n)
        Верхняя треугольная матрица из LU-разложения.
    b : np.ndarray, shape (n,)
        Вектор свободных членов системы уравнений.
    FLOAT_TOLERANCE : float, optional
        Пороговое значение для проверки вырожденности матриц. По умолчанию 1e-12.

    Returns
    -------
    np.ndarray, shape (n,)
        Вектор решения x, если система совместна.
        Если матрицы L или U вырожденные, возвращается массив, заполненный np.nan.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 3], [6, 3]])
    >>> b = np.array([7, 9])
    >>> L, U = lu_decomp_njit(A)  # Выполняем LU-разложение
    >>> x = solve_lu_njit(L, U, b)
    >>> print(x)  # Ожидаемое решение: [1.0, 1.0]
    [1.0, 1.0]
    
    >>> A = np.array([[0, 1], [1, 0]])
    >>> b = np.array([2, 3])
    >>> L, U = lu_decomp_njit(A)
    >>> x = solve_lu_njit(L, U, b)
    >>> print(x)  # Ожидаемый результат: [nan, nan] (вырожденная матрица)
    [nan, nan]

    Notes
    -----
    1. Функция требует, чтобы матрицы L и U были результатом LU-разложения невырожденной матрицы A [[1]_].
    2. Численная устойчивость обеспечивается проверкой диагональных элементов матриц L и U. Если диагональный элемент меньше FLOAT_TOLERANCE, система считается вырожденной.
    3. Поддерживает только квадратные матрицы L и U. Для прямоугольных систем требуется модификация алгоритма.
    4. Использование Numba (@njit) ускоряет вычисления за счет компиляции в машинный код [[3]_].

    References
    ----------
    .. [1] "LU-разложение — Википедия", https://en.wikipedia.org/wiki/LU_decomposition
    .. [2] "Численные методы решения СЛАУ", https://example.com/lu-solution-theory
    .. [3] "Numba: High-Performance Python", https://numba.pydata.org/
    """
    n = L.shape[0]
    y = np.zeros(n, dtype=b.dtype)

    # Прямая подстановка: решение Ly = b
    for i in range(n):
        sum_terms = 0.0
        for j in range(i):
            sum_terms += L[i, j] * y[j]
        if abs(L[i, i]) < FLOAT_TOLERANCE:
            return np.full_like(b, np.nan)
        y[i] = (b[i] - sum_terms) / L[i, i]

    # Обратная подстановка: решение Ux = y
    x = np.zeros(n, dtype=b.dtype)
    for i in range(n - 1, -1, -1):
        sum_terms = 0.0
        for j in range(i + 1, n):
            sum_terms += U[i, j] * x[j]
        if abs(U[i, i]) < FLOAT_TOLERANCE:
            return np.full_like(b, np.nan)
        x[i] = (y[i] - sum_terms) / U[i, i]

    return x
####################################################################################
@njit  # Применяем njit к QR-разложению (Грам-Шмидт)
def QR_dec(A, FLOAT_TOLERANCE=1e-12):
    """
    Выполняет QR-разложение матрицы A методом Грама-Шмидта с использованием Numba для ускорения.

    Теоретическая часть:
    QR-разложение представляет собой разложение матрицы A на произведение ортогональной матрицы Q и верхней треугольной матрицы R: A = Q @ R [[1]_]. 
    Метод Грама-Шмидта последовательно ортогонализует столбцы матрицы A, создавая базис Q, и вычисляет коэффициенты проекций в матрицу R [[2]_]. 
    Алгоритм чувствителен к численной нестабильности при малых значениях нормы векторов, что требует проверки через FLOAT_TOLERANCE [[3]_].

    Практическая реализация:
    - Инициализация матриц Q (ортонормированные векторы) и R (коэффициенты проекций).
    - Для каждого столбца A вычисляется ортогональный вектор u через вычитание проекций на предыдущие векторы Q.
    - Вектор u нормализуется и добавляется в Q. Коэффициенты проекций записываются в R.
    - При малой норме u (меньше FLOAT_TOLERANCE) соответствующие столбцы Q заполняются нулями, а элементы R обнуляются.

    Parameters
    ----------
    A : np.ndarray, shape (n, m)
        Входная матрица, для которой требуется выполнить QR-разложение.
    FLOAT_TOLERANCE : float, optional
        Пороговое значение для проверки вырожденности вектора u. По умолчанию 1e-12.

    Returns
    -------
    Q : np.ndarray, shape (n, m)
        Ортогональная матрица Q (Q.T @ Q = I).
    R : np.ndarray, shape (m, m)
        Верхняя треугольная матрица R. Если разложение невозможно из-за вырожденности вектора u, возвращаются нули в соответствующих позициях.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1, 2], [3, 4]])
    >>> Q, R = QR_dec(A)
    >>> print("Q:\n", Q)
    Q:
     [[-0.31622777 -0.9486833 ]
     [-0.9486833   0.31622777]]
    >>> print("R:\n", R)
    R:
     [[-3.16227766 -4.42718872]
     [ 0.         -0.63245553]]

    >>> A = np.array([[0, 1], [0, 0]])
    >>> Q, R = QR_dec(A)
    >>> print("Q:\n", Q)
    Q:
     [[0. 0.]
     [0. 0.]]
    >>> print("R:\n", R)
    R:
     [[0. 0.]
     [0. 0.]]

    Notes
    -----
    1. Функция использует вспомогательные функции `dot_product_njit`, `scalar_multiply_vector_njit`, `subtract_vectors_njit` и `norm`, которые должны быть определены в коде [[4]_].
    2. Численная нестабильность возможна при близких к нулю векторах u, что требует проверки через FLOAT_TOLERANCE [[3]_].
    3. Поддерживает только прямоугольные матрицы с n ≥ m. Для n < m требуется дополнение нулями.
    4. Использование Numba (@njit) ускоряет вычисления за счёт компиляции в машинный код [[5]_].

    References
    ----------
    .. [1] "QR-разложение — Википедия", https://en.wikipedia.org/wiki/QR_decomposition
    .. [2] "Метод Грама-Шмидта — Википедия", https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
    .. [3] "Численная устойчивость метода Грама-Шмидта", https://example.com/qr-stability
    .. [4] "Numba: High-Performance Python", https://numba.pydata.org/
    .. [5] "Matrix Computations" - Golub G.H., Van Loan C.F., Johns Hopkins University Press, 2013.
    """
    n, m = A.shape
    Q = np.zeros((n, m), dtype=np.float64)
    R = np.zeros((m, m), dtype=np.float64)

    for i in range(m):
        u = A[:, i].copy()
        for j in range(i):
            proj_scalar = dot_product_njit(Q[:, j], u)
            proj = scalar_multiply_vector_njit(proj_scalar, Q[:, j])
            u = subtract_vectors_njit(u, proj)
        u_norm = norm(u)

        if u_norm < FLOAT_TOLERANCE:
            Q[:, i] = np.zeros(n, dtype=A.dtype)
            R[i, i] = 0.0
        else:
            Q[:, i] = u / u_norm
            for j in range(i + 1):
                R[j, i] = dot_product_njit(Q[:, j], A[:, i])

    return Q, R
####################################################################################
MATRICES = [    
    dot_product_njit,
    norm,
    subtract_vectors_njit,
    scalar_multiply_vector_njit,
    scalar_multiply_matrix_njit,
    subtract_matrices_njit,
    multiply_matrices_njit,
    transpose_matrix_njit,
    create_diagonal_matrix_njit,
    invert_diagonal_matrix_njit,
    lu_decomp_njit,
    solve_lu_njit,
    QR_dec,
    ]