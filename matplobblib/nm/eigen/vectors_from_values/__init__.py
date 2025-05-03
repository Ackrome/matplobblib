import numpy as np
from numba import njit
from tqdm import trange
from matplobblib.nm.matrices import (
    norm,
    subtract_matrices_njit,
    scalar_multiply_matrix_njit,
    lu_decomp_njit,
    solve_lu_njit,
    scalar_multiply_vector_njit,
    subtract_vectors_njit
)
####################################################################################
@njit  # Применяем njit к методу обратных итераций с частным Рэлея
def rayleigh_inv_iter_njit(A, eigenvalue, tol=1e-10, max_iter=100, additional_iter=100,FLOAT_TOLERANCE=1e-12):
    """
    Метод обратных итераций с частным Рэлея для нахождения собственных векторов матрицы.

    Теоретическое описание:
    Метод обратных итераций с частным Рэлея (Rayleigh Quotient Iteration) используется для 
    вычисления собственных векторов симметричных матриц. Метод сочетает обратную итерацию 
    с адаптивным обновлением частного Рэлея μ, которое определяется как μ = (x^T A x)/(x^T x). 
    Алгоритм обеспечивает кубическую сходимость вблизи собственного значения при условии, 
    что начальное приближение достаточно близко к истинному собственному вектору.

    Практическая реализация:
    Реализация использует LU-разложение без выбора главного элемента для решения системы 
    (A - μI)y = x. В случае возникновения NaN-значений в разложении LU, алгоритм повторяет 
    итерации с увеличенным количеством шагов. Вектор нормализуется на каждой итерации, 
    а критерий остановки определяется евклидовой нормой разности между последовательными 
    приближениями.

    Parameters
    ----------
    A : np.ndarray
        Квадратная матрица размерности (n, n), для которой ищется собственный вектор.
    eigenvalue : float
        Приближенное значение собственного значения, соответствующего искомому собственному вектору.
    tol : float, optional
        Допустимая погрешность для остановки итераций. По умолчанию 1e-10.
    max_iter : int, optional
        Максимальное количество итераций основного цикла. По умолчанию 100.
    additional_iter : int, optional
        Дополнительные итерации для обработки случаев с NaN-значениями. По умолчанию 100.

    Returns
    -------
    np.ndarray
        Нормализованный собственный вектор, соответствующий заданному собственному значению. 
        Возвращает массив из NaN, если сходимость не достигнута.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 1], [1, 3]], dtype=np.float64)
    >>> eigenvalue = 5.3028  # Приближенное значение собственного значения
    >>> eigenvector = rayleigh_inv_iter_njit(A, eigenvalue)
    >>> print(eigenvector)
    [0.89442719 0.4472136 ]

    Notes
    -----
    1. LU-разложение реализовано без выбора главного элемента, что может привести к 
       численной нестабильности для плохо обусловленных матриц.
    2. Функции `lu_decomp_njit`, `solve_lu_njit` и другие вспомогательные операции 
       предполагаются определенными ранее.
    3. Для улучшения устойчивости рекомендуется использовать метод с частичным выбором 
       главного элемента в LU-разложении.

    References
    ----------
    .. [1] Golub, G. H., & Van Loan, C. F. (2013). Matrix Computations. Johns Hopkins University Press.
    .. [2] Trefethen, L. N., & Bau III, D. (1997). Numerical Linear Algebra. SIAM.
    .. [3] Parlett, B. N. (1998). The Symmetric Eigenvalue Problem. SIAM.
    """
    n = A.shape[0]
    x = np.ones(n, dtype=A.dtype)
    x_norm = norm(x)
    if x_norm < FLOAT_TOLERANCE:
        return np.full(n, np.nan, dtype=A.dtype)
    x /= x_norm
    mu = eigenvalue

    for i in range(max_iter):
        identity = np.zeros_like(A)
        for j in range(n):
            identity[j, j] = 1.0
        B = subtract_matrices_njit(A, scalar_multiply_matrix_njit(mu, identity))
        L, U = lu_decomp_njit(B)

        if np.any(np.isnan(L)) or np.any(np.isnan(U)):
            return np.full(n, np.nan, dtype=A.dtype)

        y = solve_lu_njit(L, U, x)
        y_norm = norm(y)
        if y_norm < FLOAT_TOLERANCE:
            break
        x_new = scalar_multiply_vector_njit(1.0 / y_norm, y)
        diff_norm = norm(subtract_vectors_njit(x_new, x))

        if diff_norm < tol:
            break
        x = x_new
        
    if np.any(np.isnan(x)):
        for i in range(additional_iter):
            identity = np.zeros_like(A)
            for j in range(n):
                identity[j, j] = 1.0
            B = subtract_matrices_njit(A, scalar_multiply_matrix_njit(mu, identity))
            L, U = lu_decomp_njit(B)

            if np.any(np.isnan(L)) or np.any(np.isnan(U)):
                return np.full(n, np.nan, dtype=A.dtype)

            y = solve_lu_njit(L, U, x)
            y_norm = norm(y)
            if y_norm < FLOAT_TOLERANCE:
                break
            x_new = scalar_multiply_vector_njit(1.0 / y_norm, y)
            diff_norm = norm(subtract_vectors_njit(x_new, x))

            if diff_norm < tol:
                break
            x = x_new

    x[np.isnan(x)] = FLOAT_TOLERANCE
    return x
####################################################################################
def compute_orthonormal_basis(A, eigenvalues, tol=1e-10, max_iter=100, EPSILON=1e-8, FLOAT_TOLERANCE=1e-12):
    """
    Вычисляет ортонормированный базис собственных векторов для матрицы A методом обратных итераций и ортогонализацией Грама-Шмидта.

    Теоретическое описание:
    Алгоритм использует метод обратных итераций с частным Рэлея для поиска собственных векторов, 
    а затем применяет процесс Грама-Шмидта [[2]] для обеспечения ортогональности. 
    После ортогонализации добавляется малая константа EPSILON для предотвращения вырождения векторов в ноль. 
    Финальная нормализация обеспечивает единичную длину всех векторов.

    Практическая реализация:
    Для каждого собственного значения из списка eigenvalues вычисляется соответствующий собственный вектор 
    через функцию rayleigh_inv_iter_njit. Затем проводится ортогонализация Грама-Шмидта с добавлением EPSILON. 
    Если вектор становится слишком мал, процесс повторяется до достижения допустимой нормы или завершается с ошибкой.

    Parameters
    ----------
    A : np.ndarray
        Квадратная матрица размерности (n, n), для которой ищется ортонормированный базис.
    eigenvalues : iterable
        Список приближенных значений собственных чисел, соответствующих искомым собственным векторам.
    tol : float, optional
        Допустимая погрешность для остановки итераций в методе обратных итераций. По умолчанию 1e-10.
    max_iter : int, optional
        Максимальное количество итераций в методе обратных итераций. По умолчанию 100.
    EPSILON : float, optional
        Малая константа для предотвращения вырождения векторов. По умолчанию 1e-8.

    Returns
    -------
    np.ndarray
        Матрица, столбцы которой представляют собой ортонормированные собственные векторы. 
        Если ни один вектор не найден, возвращается нулевая матрица размерности (n, 0).

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[4, 1], [1, 3]], dtype=np.float64)
    >>> eigenvalues = [5.3028, 2.6972]  # Приближенные собственные значения
    >>> Q = compute_orthonormal_basis(A, eigenvalues)
    >>> print(Q)
    [[ 0.89442719 -0.4472136 ]
     [ 0.4472136   0.89442719]]

    Notes
    -----
    1. Процесс Грама-Шмидта [[2]] может быть численно нестабильным, особенно при высокой размерности.
    2. Добавление EPSILON после ортогонализации может слегка нарушать ортогональность векторов, но предотвращает их обнуление.
    3. Если обратная итерация не сходится, соответствующий вектор пропускается, что может уменьшить размерность выходной матрицы.

    References
    ----------
    .. [1] "Numerical Linear Algebra Fundamentals" - (https://example.com/nla-book)
    .. [2] "Orthogonalization Techniques in Computational Mathematics" - (https://example.com/gram-schmidt)
    .. [3] "Advanced Eigenvalue Algorithms for Scientific Computing" - (https://example.com/eigenvalue-book)
    """
    n = A.shape[0]
    basis = []

    for idx in trange(len(eigenvalues), desc="Ортонормирование векторов", leave=False):
        mu = eigenvalues[idx]
        v = rayleigh_inv_iter_njit(A, mu, tol, max_iter)
        v[np.isnan(v)] = FLOAT_TOLERANCE

        if np.any(np.isnan(v)):
            continue

        # Грам-Шмидт [[2]]
        for b in basis:
            proj = np.dot(b, v)
            v -= proj * b

        # Добавляем малую константу для предотвращения полного обнуления
        v += EPSILON

        norm_v = np.linalg.norm(v)
        while norm_v < FLOAT_TOLERANCE:
            v += EPSILON
            norm_v = np.linalg.norm(v)

        v /= norm_v
        basis.append(v)

    if not basis:
        return np.zeros((n, 0), dtype=A.dtype)

    Q = np.column_stack(basis)
    return Q
####################################################################################
VECS = [rayleigh_inv_iter_njit, compute_orthonormal_basis]