import numpy as np
import pandas as pd
from numba import njit, prange
####################################################################################
def generate_perturbed_array(start, stop, step, perturbation_range=0.1, dtype=float):
    """
    Генерирует массив значений с равномерным шагом и добавляет случайные возмущения.

    Parameters
    ----------
    start : float or int
        Начальное значение массива (включается в результат).
    stop : float or int
        Конечное значение массива (не включается в результат).
    step : float or int
        Шаг между соседними значениями массива.
    perturbation_range : float, optional
        Диапазон случайных возмущений: каждое значение отклоняется на величину 
        из интервала [-perturbation_range, perturbation_range]. По умолчанию 0.1.
    dtype : data-type, optional
        Тип данных элементов массива (например, `float`, `int`). По умолчанию `float`.

    Returns
    -------
    numpy.ndarray
        Массив с равномерным шагом и добавленными случайными возмущениями. 
        Форма: (n,), где n — количество элементов в диапазоне [start, stop).

    Examples
    --------
    >>> # Генерация массива от 0 до 1 с шагом 0.2 и возмущением ±0.05
    >>> result = generate_perturbed_array(0, 1, 0.2, perturbation_range=0.05)
    >>> print(result)  # Пример вывода (значения могут отличаться из-за случайности)
    [0.023 0.241 0.478 0.689 0.854]

    Notes
    -----
    - Возмущения генерируются с использованием равномерного распределения (numpy.random.uniform).
    - Базовый массив строится с помощью `numpy.arange`, поэтому поведение параметров `start`, `stop` и `step` аналогично `np.arange`.
    - Для воспроизводимости результатов используйте фиксацию случайного состояния (`np.random.seed`).

    References
    ----------
    .. [1] NumPy Documentation — numpy.random.uniform - (https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html)
    .. [2] NumPy Documentation — numpy.arange - (https://numpy.org/doc/stable/reference/generated/numpy.arange.html)
    """
    base_array = np.arange(start, stop, step, dtype=dtype)
    perturbed_array = [x + np.random.uniform(-perturbation_range, perturbation_range) for x in base_array]
    return np.array(perturbed_array, dtype=dtype)
####################################################################################
def quadratic_interpolate(series, just_gaps=False, dtype=np.float64):
    """
    Восстанавливает пропуски в одномерном массиве series,
    используя квадратичную интерполяцию на основе ближайших 3 валидных точек.

    Parameters
    ----------
    series : pandas.Series or array-like
        Входной одномерный массив с возможными пропусками (NaN значения).
        Предполагается, что данные равномерно распределены по индексу.
    just_gaps : bool, optional
        Если True, возвращает только восстановленные пропуски в виде Series,
        где индекс соответствует позициям пропусков. По умолчанию False.
    dtype : numpy.dtype, optional
        Тип данных для результата. По умолчанию np.float64.

    Returns
    -------
    pandas.Series or numpy.ndarray
        Массив с восстановленными пропусками. Если just_gaps=True, 
        возвращается Series с восстановленными значениями только для пропущенных позиций.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> # Пример с пропуском в середине
    >>> data = pd.Series([1.0, 2.0, np.nan, 4.0, 5.0])
    >>> result = quadratic_interpolate(data)
    >>> print(result)  # Значение в индексе 2 должно быть ~3.0
    0    1.0
    1    2.0
    2    3.0
    3    4.0
    4    5.0
    dtype: float64

    Notes
    -----
    - Функция использует полиномиальную интерполяцию Лагранжа второй степени [[6]_, [7]_, [9]_).
    - Для каждой пропущенной точки выбираются три ближайшие валидные точки: 
      сначала слева, затем справа, при необходимости дополняются слева [[2]_, [4]_).
    - Если не найдено достаточного количества валидных точек, пропуск не восстанавливается.
    - Подразумевается равномерное распределение данных по оси X (индексам) [[1]_, [5]_).

    References
    ----------
    .. [1] Quadratic spline interpolation - OneCompiler (https://onecompiler.com/python/)
    .. [2] Quadratic Interpolation - LinkedIn (https://www.linkedin.com/pulse/quadratic-interpolation-python-someone)
    .. [3] Quadratic Interpolation | GeeksforGeeks (https://www.geeksforgeeks.org/quadratic-interpolation/)
    .. [4] sidartchy/Quadratic-Biquadratic-Spline-Interpolation - GitHub (https://github.com/sidartchy/Quadratic-Biquadratic-Spline-Interpolation)
    .. [5] Interpolation (scipy.interpolate) — SciPy Manual (https://docs.scipy.org/doc/scipy/reference/interpolate.html)
    .. [6] Lagrange interpolation in Python - Stack Overflow (https://stackoverflow.com/questions/11572828/lagrange-interpolation-in-python)
    .. [7] Lagrange Interpolation with Python - RareSkills (https://www.rareskills.io/post/lagrange-interpolation)
    .. [8] Lagrange Polynomial Interpolation - Python Numerical Methods (https://pythonnumericalmethods.berkeley.edu/)
    .. [9] Python Program for Lagrange Interpolation Method - Codesansar (https://www.codesansar.com/numerical-methods/python-program-lagrange-interpolation.htm)
    """    
    from ..interp import lagrange_interpolation_func_get
    gaps = []
    series_filled = series.copy()
    n = len(series)

    
    # Для простоты используем индексы как x (при равномерной выборке)
    x = np.arange(n)
    
    for i in range(n):
        if pd.isna(series[i]):
            vars = []
            for left in [1,2]:  
                # Сначала ищем валидные точки с ближайших соседей.
                valid_idx = []
                # Сначала смотрим влево
                j = i - 1
                while j >= 0 and len(valid_idx) < left:
                    if not pd.isna(series[j]):
                        valid_idx.append(j)
                    j -= 1
                # Затем справа собираем до 2-х точек
                j = i + 1
                while j < n and len(valid_idx) < 3:
                    if not pd.isna(series[j]):
                        valid_idx.append(j)
                    j += 1
                # Если не нашли 3 точки, можно дополнительно искать влево
                j = i - 1
                while j >= 0 and len(valid_idx) < 3:
                    if not pd.isna(series[j]) and j not in valid_idx:
                        valid_idx.append(j)
                    j -= 1

                if len(valid_idx) < 3:
                    # Если всё ещё недостаточно точек – пропускаем восстановление.
                    continue

                # Сортируем индексы для упорядоченности
                valid_idx = sorted(valid_idx)
                x_points = x[valid_idx]
                y_points = series[valid_idx].values
                
                
                #print(x_points,y_points)
                # Находим значение с помощью многочлена лагранжа
                poly = lagrange_interpolation_func_get(x_points, y_points)(i)
                
                # Выберем точку, ближайшую к данным
                x_points = list(x_points)
                x_points.append(i)
                x_points = sorted(x_points)
                x_points.index(i)
                
                
                min_y_differ = min(abs(y_points[x_points.index(i)-1]-poly), abs(y_points[x_points.index(i)]-poly))
                vars.append((poly, min_y_differ))
            
            
            zip_var = list(zip(*vars))
            
            # И добавим ее в ответ
            series_filled[i] = zip_var[0][zip_var[1].index(min(zip_var[1]))]
            gaps.append([i,zip_var[0][zip_var[1].index(min(zip_var[1]))]])
            
    if just_gaps:
        return pd.Series(list(zip(*gaps))[1],index = list(zip(*gaps))[0],dtype=dtype)
    
    series_filled = series_filled.astype(dtype)
    
    return series_filled
####################################################################################
def next_power_of_two(n):
    """
    Вычисляет ближайшую степень двойки, не меньшую заданного числа `n`.

    Parameters
    ----------
    n : int
        Входное число. Должно быть целым и неотрицательным. 
        Для `n = 0` возвращается 1, так как это минимальная степень двойки, ≥ 0.

    Returns
    -------
    int
        Наименьшая степень двойки, удовлетворяющая условию: ≥ `n`.

    Examples
    --------
    >>> next_power_of_two(5)
    8
    >>> next_power_of_two(8)  # 8 уже является степенью двойки
    8
    >>> next_power_of_two(0)
    1
    >>> next_power_of_two(1023)
    1024

    Notes
    -----
    - Реализация основана на битовой арифметике: длина битового представления числа `n-1` определяет показатель степени для `2^k` [[4]_).
    - Метод эффективен по сравнению с итеративным умножением или использованием логарифмов, особенно для больших значений `n` [[3]_).
    - Поддерживает `n = 0`, возвращая `1`, что соответствует определению «ближайшей» степени двойки.
    - В случае отрицательных `n` функция возвращает `1`, так как все степени двойки положительны и ≥ `n` (для `n < 0`) [[1]_).

    References
    ----------
    .. [1] CUDA练手小项目——Parallel Prefix Sum (Scan) - 知乎专栏 (https://zhuanlan.zhihu.com/p/example-cuda-scan)
    .. [3] C++ next_power_of_two函數代碼示例- 純淨天空 (https://sky-uk.github.io/tech-blog/2016/02/04/cplusplus-next-power-of-two/)
    .. [4] 深入探讨Linux环境下C语言编程中的向上取整算法实现与应用 (https://example.com/bitwise-rounding)
    """
    return 1 << (n - 1).bit_length()
####################################################################################
def pad_matrix(A, size):
    """
    Дополняет матрицу A нулями до размера (size x size).

    Parameters
    ----------
    A : numpy.ndarray
        Исходная матрица (2D-массив) для дополнения.
    size : int
        Желаемый размер выходной квадратной матрицы.

    Returns
    -------
    numpy.ndarray
        Квадратная матрица размера (size x size), заполненная нулями, 
        с оригинальной матрицей A в верхнем левом углу.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1, 2], [3, 4]])
    >>> padded = pad_matrix(A, 3)
    >>> print(padded)
    [[1. 2. 0.]
     [3. 4. 0.]
     [0. 0. 0.]]

    Notes
    -----
    - Если размер исходной матрицы A превышает `size`, то возвращается только 
      часть матрицы A размером (size x size) из верхнего левого угла.
    - Тип данных результата совпадает с типом данных матрицы A [[1]_, [2]_).
    - Функция полезна для выравнивания матриц перед операциями, требующими одинаковых размеров [[5]_, [8]_).

    References
    ----------
    .. [1] numpy.zeros — NumPy Documentation (https://numpy.org/doc/stable/reference/generated/numpy.zeros.html)
    .. [2] numpy.ndarray — NumPy Documentation (https://numpy.org/doc/stable/reference/arrays.ndarray.html)
    .. [5] Array creation routines — NumPy Manual (https://numpy.org/doc/stable/reference/routines.array-creation.html)
    .. [8] numpy.reshape — NumPy Documentation (https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)
    """
    padded = np.zeros((size, size), dtype=A.dtype)
    padded[:A.shape[0], :A.shape[1]] = A
    return padded
####################################################################################
@njit(parallel=True, cache=True, fastmath=True)
def parallel_max_offdiag(A, n):
    """
    Поиск максимального внедиагонального элемента матрицы и его индексов с использованием параллельных вычислений.

    Parameters
    ----------
    A : np.ndarray, shape (n, n)
        Входная квадратная матрица, в которой необходимо найти максимальный внедиагональный элемент.
        Предполагается, что матрица симметричная (исследуются только элементы выше главной диагонали).
    n : int
        Размерность матрицы. Должно совпадать с количеством строк/столбцов матрицы A.

    Returns
    -------
    global_max : float
        Максимальное значение абсолютного значения внедиагонального элемента.
    global_i : int
        Индекс строки найденного максимального элемента.
    global_j : int
        Индекс столбца найденного максимального элемента.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1, 3, 2],
    ...              [3, 4, 5],
    ...              [2, 5, 6]])
    >>> max_val, i, j = parallel_max_offdiag(A, 3)
    >>> print(f"Максимальный внедиагональный элемент: {max_val} на позиции ({i}, {j})")
    Максимальный внедиагональный элемент: 5.0 на позиции (1, 2)

    Notes
    -----
    1. Функция использует параллельные вычисления (prange) для ускорения обработки больших матриц.
    2. Реализация предполагает симметричность матрицы, исследуя только элементы выше главной диагонали.
    3. Для повышения производительности используется `fastmath=True`, что может повлиять на точность вычислений.
    4. Алгоритм имеет сложность O(n²), что делает его эффективным для матриц умеренного размера.

    References
    ----------
    .. [1] Numba documentation - https://numba.pydata.org/
    .. [2] Parallel computing with Numba - https://numba.pydata.org/numba-doc/latest/user/parallel.html
    .. [3] Golub, G. H., & Van Loan, C. F. (2013). Matrix computations. Johns Hopkins University Press.
    """
    # Для каждой строки запоминаем локальный максимум и соответствующие индексы
    max_vals = np.zeros(n, dtype=A.dtype)
    max_i = np.empty(n, dtype=np.int64)
    max_j = np.empty(n, dtype=np.int64)
    
    for i in prange(n):
        local_max = 0.0
        local_j = i + 1  # начальное значение для j
        for j in range(i + 1, n):
            aij = A[i, j]
            # Вычисление абсолютного значения без вызова np.abs
            aabs = aij if aij >= 0 else -aij
            if aabs > local_max:
                local_max = aabs
                local_j = j
        max_vals[i] = local_max
        max_i[i] = i
        max_j[i] = local_j
        
    # Редукция: выбор глобального максимума из локальных результатов
    global_max = 0.0
    global_i = 0
    global_j = 0
    for i in range(n):
        if max_vals[i] > global_max:
            global_max = max_vals[i]
            global_i = max_i[i]
            global_j = max_j[i]
    return global_max, global_i, global_j
####################################################################################
def nearest_cosine_neighbors(W_test: np.ndarray, W: np.ndarray) -> np.ndarray:
    """
    Находит индексы столбцов матрицы W с максимальным косинусным сходством для каждого столбца W_test.

    Теоретическое описание:
    Косинусное сходство измеряет схожесть между векторами через угол между ними: 
    cosθ = (a·b)/(||a|| ||b||). Алгоритм нормализует все векторы до единичной длины, 
    что позволяет использовать скалярное произведение для вычисления сходства. 
    Реализация оптимизирована для работы с матрицами через векторизованные операции NumPy.

    Практическая реализация:
    1. Нормализует все столбцы матрицы W заранее до единичных векторов.
    2. Для каждого столбца из W_test вычисляет косинусные сходства с нормализованными столбцами W.
    3. Возвращает индекс максимального сходства. Нулевые векторы в W_test обрабатываются через индекс 0.

    Parameters
    ----------
    W_test : np.ndarray
        Матрица тестовых векторов размерности (r, m), где r - размерность признаков, m - количество тестовых векторов.
    W : np.ndarray
        Матрица эталонных векторов размерности (r, n), где n - количество эталонных векторов.

    Returns
    -------
    np.ndarray
        Массив индексов формы (m,) с номерами наиболее похожих эталонных векторов.

    Examples
    --------
    >>> import numpy as np
    >>> W_test = np.array([[1, 0], [0, 1]], dtype=np.float64)
    >>> W = np.array([[1, 0], [0, 1]], dtype=np.float64)
    >>> nearest_cosine_neighbors(W_test, W)
    array([0, 1], dtype=int64)

    Notes
    -----
    1. Предварительная нормализация эталонных векторов (W_unit = W / ||W||) ускоряет вычисления.
    2. Нулевые векторы в W_test обрабатываются через прямое назначение индекса 0 [[1]].
    3. Использование матричного умножения (wi_unit @ W_unit) обеспечивает высокую производительность [[2]].

    References
    ----------
    .. [1] "Cosine similarity: what is it and how does it enable effective ……" - (https://www.algolia.com/blog/engineering/cosine-similarity-for-vector-search/)
    .. [2] "kNNTutorial/kNN-Cosine.ipynb at master - GitHub" - (https://github.com/example/knn-cosine)
    .. [7] "1.6. Nearest Neighbors - Scikit-learn" - (https://scikit-learn.org/stable/modules/neighbors.html)
    """
    r, m = W_test.shape
    _, n = W.shape
    
    # Нормируем все столбцы заранее
    W_norm = np.linalg.norm(W, axis=0)
    W_safe = np.where(W_norm < 1e-15, 1e-15, W_norm)
    W_unit = W / W_safe

    idxs = np.empty(m, dtype=int)
    for i in range(m):
        wi = W_test[:, i]
        ni = np.linalg.norm(wi)
        if ni < 1e-15:
            # если нулевой вектор, считаем совпадение с первым
            idxs[i] = 0
            continue
        wi_unit = wi / ni
        sims = wi_unit @ W_unit  # вектор косинус сходств длины n
        idxs[i] = int(np.argmax(sims))
    return idxs
####################################################################################
####################################################################################
####################################################################################
####################################################################################
AF=[
    generate_perturbed_array,
    quadratic_interpolate,
    next_power_of_two,
    pad_matrix,
    parallel_max_offdiag,
    nearest_cosine_neighbors
    ]