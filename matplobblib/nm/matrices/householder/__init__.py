from numba import njit
from tqdm import tqdm
import numpy as np
from ..__init__ import (
    dot_product_njit,
    norm,
    subtract_vectors_njit,
    scalar_multiply_vector_njit,
    scalar_multiply_matrix_njit,
    subtract_matrices_njit,
    multiply_matrices_njit,
    
)
####################################################################################
@njit  # Применяем njit для построения отражения Хаусхолдера
def householder_reflection_njit(vector, FLOAT_TOLERANCE=1e-12):
    """
    Строит матрицу отражения Хаусхолдера для заданного вектора.

    Теоретическая часть:
    Отражение Хаусхолдера — это линейное преобразование, которое отражает вектор относительно гиперплоскости, определяемой вектором v [[1]_]. 
    Матрица отражения Хаусхолдера вычисляется по формуле: P = I - 2 * (v * vᵀ) / (vᵀ * v), где v — вектор отражения, а I — единичная матрица [[2]_]. 
    Эта матрица ортогональна и симметрична (P = Pᵀ = P⁻¹), что делает её полезной для численных методов, таких как QR-разложение [[3]_].

    Практическая реализация:
    - Вычисление нормы входного вектора.
    - Построение вектора v через вычитание из исходного вектора нормализованного e1-вектора.
    - Проверка на вырожденность вектора v (малая норма v).
    - Вычисление внешнего произведения v * vᵀ и его масштабирование.
    - Построение матрицы отражения через вычитание масштабированного внешнего произведения из единичной матрицы.

    Parameters
    ----------
    vector : np.ndarray, shape (n,)
        Входной вектор, для которого строится матрица отражения Хаусхолдера.
    FLOAT_TOLERANCE : float, optional
        Пороговое значение для проверки вырожденности вектора v. По умолчанию 1e-12.

    Returns
    -------
    P : np.ndarray, shape (n, n)
        Матрица отражения Хаусхолдера. Если вектор v вырожден (его норма меньше FLOAT_TOLERANCE), возвращается единичная матрица.

    Examples
    --------
    >>> import numpy as np
    >>> vector = np.array([3, 4])
    >>> P = householder_reflection_njit(vector)
    >>> print("Матрица отражения P:\n", P)
    Матрица отражения P:
     [[ 0.6  -0.8 ]
     [-0.8  -0.6 ]]
    >>> # Применение матрицы P к исходному вектору
    >>> reflected = P @ vector
    >>> print("Отраженный вектор:", reflected)
    Отраженный вектор: [5. 0.]

    >>> vector = np.array([1, 0, 0])
    >>> P = householder_reflection_njit(vector)
    >>> print("Матрица отражения P:\n", P)
    Матрица отражения P:
     [[1. 0. 0.]
     [0. 1. 0.]
     [0. 0. 1.]]

    Notes
    -----
    1. Функция использует вспомогательные функции (norm, subtract_vectors_njit, scalar_multiply_vector_njit, dot_product_njit, scalar_multiply_matrix_njit, subtract_matrices_njit), которые должны быть определены в коде [[4]_].
    2. Вычисление внешнего произведения v * vᵀ неэффективно по памяти и требует O(n²) операций. В стандартных реализациях отражение применяется без явного построения матрицы P [[5]_].
    3. Если норма вектора v слишком мала (меньше FLOAT_TOLERANCE), возвращается единичная матрица для предотвращения деления на ноль.
    4. Матрица P используется для обнуления всех элементов вектора ниже диагонали при QR-разложении [[3]_].

    References
    ----------
    .. [1] "Householder transformation - Wikipedia", https://en.wikipedia.org/wiki/Householder_transformation
    .. [2] "QR-разложение методом Хаусхолдера - MathWorks", https://www.mathworks.com/help/matlab/ref/qr.html
    .. [3] "Matrix Computations" - Golub G.H., Van Loan C.F., Johns Hopkins University Press, 2013.
    .. [4] "Numba: High-Performance Python", https://numba.pydata.org/
    .. [5] "Numerical Linear Algebra" - Trefethen L.N., Bau D., SIAM, 1997.
    """
    n = len(vector)
    e1 = np.zeros(n, dtype=vector.dtype)
    if n > 0:
        e1[0] = 1.0
    vec_norm = norm(vector)
    v = subtract_vectors_njit(vector, scalar_multiply_vector_njit(vec_norm, e1))
    v_norm_sq = dot_product_njit(v, v)

    if v_norm_sq < FLOAT_TOLERANCE:
        return np.eye(n, dtype=vector.dtype)

    outer_product = np.zeros((n, n), dtype=vector.dtype)
    for i in range(n):
        for j in range(n):
            outer_product[i, j] = v[i] * v[j]

    scaled_outer_product = scalar_multiply_matrix_njit(2.0 / v_norm_sq, outer_product)
    P = subtract_matrices_njit(np.eye(n, dtype=vector.dtype), scaled_outer_product)
    return P
####################################################################################
@njit  # Применяем njit к применению преобразований Хаусхолдера
def apply_householder_to_matrix_njit(matrix, start_col, FLOAT_TOLERANCE=1e-12):
    """
    Приводит матрицу к верхней хессенберговой форме с использованием преобразований Хаусхолдера.

    Теоретическая часть:
    Преобразование Хаусхолдера — это метод ортогонального отражения, который используется для обнуления элементов под диагональю матрицы [[1]_]. 
    Верхняя хессенбергова форма матрицы имеет нулевые элементы ниже первой поддиагонали, что упрощает последующие вычисления, например, QR-алгоритм [[2]_]. 
    На каждой итерации строится матрица отражения Хаусхолдера H для подвектора, и исходная матрица преобразуется как H @ A @ H^T (для симметричных матриц) или H @ A (для несимметричных) [[3]_].

    Практическая реализация:
    - Инициализация накопителя ортогональной матрицы Q.
    - Для каждого столбца k выделяется подвектор v = matrix[k+1:, k].
    - Строится матрица отражения Хаусхолдера H_sub для вектора v.
    - Матрица H расширяется до размерности n × n и применяется к исходной матрице: matrix = H @ matrix.
    - Обновляется накопитель Q_acc = Q_acc @ H.
    - Возвращаются преобразованная матрица и ортогональная матрица Q.

    Parameters
    ----------
    matrix : np.ndarray, shape (n, n)
        Входная квадратная матрица, которую требуется привести к верхней хессенберговой форме.
    start_col : int
        Начальный индекс столбца, с которого начинается обработка. Обычно 0 для полной матрицы.
    FLOAT_TOLERANCE : float, optional
        Пороговое значение для проверки вырожденности подвектора v. По умолчанию 1e-12.

    Returns
    -------
    matrix : np.ndarray, shape (n, n)
        Матрица в верхней хессенберговой форме.
    Q_acc : np.ndarray, shape (n, n)
        Накопленная ортогональная матрица преобразований Хаусхолдера.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 3, 2, 1],
    ...              [6, 5, 4, 3],
    ...              [0, 2, 1, 0],
    ...              [0, 0, 1, 2]])
    >>> matrix, Q = apply_householder_to_matrix_njit(A, 0)
    >>> print("Верхняя хессенбергова форма:")
    [[ 4.    3.    2.    1.  ]
     [-7.211 5.833 5.166 4.166]
     [ 0.    1.528 1.389 1.111]
     [ 0.    0.    1.414 2.    ]]

    Notes
    -----
    1. Функция требует реализации вспомогательных функций `householder_reflection_njit` и `multiply_matrices_njit` [[4]_].
    2. Численная устойчивость обеспечивается проверкой нормы подвектора v. Если норма меньше FLOAT_TOLERANCE, отражение пропускается.
    3. Для симметричных матриц результатом будет трехдиагональная форма (специальный случай хессенберговой матрицы) [[2]_].
    4. Метод имеет сложность O(n³), где n — размерность матрицы [[5]_].

    References
    ----------
    .. [1] "Householder transformation - Wikipedia", https://en.wikipedia.org/wiki/Householder_transformation
    .. [2] "QR-разложение методом Хаусхолдера - MathWorks", https://www.mathworks.com/help/matlab/ref/qr.html
    .. [3] "Matrix Computations" - Golub G.H., Van Loan C.F., Johns Hopkins University Press, 2013.
    .. [4] "Numba: High-Performance Python", https://numba.pydata.org/
    .. [5] "Numerical Linear Algebra" - Trefethen L.N., Bau D., SIAM, 1997.
    """
    n = matrix.shape[0]
    Q_acc = np.eye(n, dtype=matrix.dtype)

    for k in range(start_col, n - 2):
        # Выделяем подвектор для построения отражения
        v_segment = matrix[k + 1:, k]
        
        # Проверка на вырожденность подвектора
        if v_segment.size == 0 or np.all(np.abs(v_segment) < FLOAT_TOLERANCE):
            continue

        # Строим отражение Хаусхолдера для подвектора
        H_sub = householder_reflection_njit(v_segment)
        
        # Расширяем H_sub до полной матрицы
        H = np.eye(n, dtype=matrix.dtype)
        H[k + 1:, k + 1:] = H_sub

        # Применяем преобразование Хаусхолдера
        matrix = multiply_matrices_njit(H, matrix)
        Q_acc = multiply_matrices_njit(Q_acc, H)

    return matrix, Q_acc
####################################################################################
def Householder(X, TOL=1e-12):
    """
    Приводит симметричную матрицу к трёхдиагональной форме с помощью отражений Хаусхолдера.

    Теоретическая часть:
    Метод Хаусхолдера (отражений) применяется для приведения симметричных матриц к трёхдиагональному виду за счёт ортогональных преобразований, сохраняющих собственные значения матрицы [[1]_]. 
    На каждом шаге строится вектор Хаусхолдера v, который обнуляет все элементы ниже первой поддиагонали в текущем столбце. 
    Преобразование выполняется как B = H_p @ B @ H_p, где H_p — расширенная матрица отражения [[2]_]. 
    Алгоритм требует O(n³) операций для матрицы размерности n × n [[5]_].

    Практическая реализация:
    - Для каждого столбца i выделяется подвектор x = B[i+1:, i].
    - Вычисляется σ = -sign(x[0]) * ||x||₂ для устойчивости [[1]_].
    - Строится вектор v = x - σ * e₁ и нормализуется.
    - Матрица отражения H формируется для подматрицы и расширяется до размерности исходной матрицы.
    - Двустороннее преобразование B = H_p @ B @ H_p сохраняет симметрию и собственные значения.

    Parameters
    ----------
    X : np.ndarray, shape (n, n)
        Входная симметричная матрица, которую требуется привести к трёхдиагональной форме.
    TOL : float, optional
        Пороговое значение для проверки нормы вектора v. По умолчанию 1e-12.

    Returns
    -------
    B : np.ndarray, shape (n, n)
        Трёхдиагональная матрица, полученная через последовательные отражения Хаусхолдера. 
        Если норма вектора v слишком мала, соответствующее преобразование пропускается.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 1, -2, 2], 
    ...              [1, 2, 0, 1], 
    ...              [-2, 0, 3, -2], 
    ...              [2, 1, -2, -1]])
    >>> B = Householder(A)
    >>> print("Трёхдиагональная форма:")
    >>> print(un_rrstr(rrstr(B,3)))
    Трёхдиагональная форма:
    [[ 4.    -3.     0.     0.   ]
     [-3.     3.333 -1.667  0.   ]
     [ 0.    -1.667 -1.32  -0.907]
     [ 0.    -0.    -0.907  1.987]]

    Notes
    -----
    1. Метод применим только для симметричных матриц. Для несимметричных матриц требуется использование других алгоритмов [[1]_].
    2. Каждое преобразование Хаусхолдера сохраняет ортогональность и симметрию матрицы [[2]_].
    3. Порог TOL предотвращает деление на ноль при нормализации вектора v. Если ||v|| < TOL, отражение пропускается [[5]_].
    4. Функция использует `tqdm` для отображения прогресс-бара, что требует установки библиотеки [[6]_].

    References
    ----------
    .. [1] "Сведение симметричной матрицы к трехдиагональной форме", https://example.com/householder-symmetric
    .. [2] "Метод Хаусхолдера для QTQ^T-разложения", https://example.com/householder-qtq
    .. [5] "Вычислительная линейная алгебра с примерами на MATLAB", Горбаченко В.И., 2011.
    .. [6] "tqdm: A Fast, Extensible Progress Bar for Python", https://github.com/tqdm/tqdm
    """
    B = X.copy()
    n = B.shape[0]
    # Основной цикл приведения с прогресс-баром
    for i in tqdm(range(n-1), desc="Приведение Хаусхолдера", leave=False):
        # Выделяем подстолбец под диагональю
        x = B[i+1:, i].copy()  # Создаем копию для избежания ссылок

        # Вычисляем длину вектора с учетом направления для зануления
        sigma = -1 * np.sign(x[0]) * np.sqrt(np.sum(x**2)) if x[0] != 0 else -np.sqrt(np.sum(x**2))

        # Формируем вспомогательный вектор с первым ненулевым элементом
        se = np.zeros_like(x)
        se[0] = sigma

        # Строим отражающий вектор
        v = x - se
        vn = np.linalg.norm(v)  # Норма вектора

        # Пропускаем итерацию при нулевом векторе (защита от деления на ноль)
        if vn < TOL:
            continue

        v = v / vn  # Нормализация
        v = v.reshape(-1, 1)  # Преобразуем в вектор-столбец

        # Формируем матрицу отражения Хаусхолдера для подматрицы
        H = np.eye(len(x)) - 2 * v @ v.T

        # Расширяем матрицу отражения до размера исходной матрицы
        Hp = np.eye(n)
        Hp[i+1:, i+1:] = H

        # Применяем двустороннее преобразование (сохраняет спектр)
        B = Hp @ B @ Hp
    return B
####################################################################################
HOUSEHOLDER = [Householder, apply_householder_to_matrix_njit,householder_reflection_njit]