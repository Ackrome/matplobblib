
```python
import numpy as np
```
# решение уравнений

## newton


```python
def modified_newton(f, df, x, x0, tol): # модифицированный метод касательных
    '''
    Модифицированный метод Ньютона: еа каждом шаге использует производную, вычисленную на первом шаге
    Можжно сделать, чтобы производная каждый раз считалась новая => самая высокая сходимость
    '''
    x_new = x - f(x)/df(x0) # определяем новую точку
    if abs(x_new-x)<tol: # проверяем, достигнута ли требуемая точность - если да, то возвращаем новый x
        return x_new
    return modified_newton(f, df, x_new, x0, tol) # если нет - делаем ещё один шаг
```
## итераций


```python
def g(x):
    '''
    Определение функции g для меода итераций
    Коэффициенты a и b подбираются для сходимости из условия:
    |g(x)|<1
    '''
    g = np.zeros_like(x)

    g[0] = x[0] - a*f1(x)
    g[1] = x[1] - b*f2(x)
    
    return g
```

```python
def f_iteration(g, x0, n_iterations=20):
    iters = np.zeros((n_iterations+1, len(x0)))
    iters[0, :] = x0
    
    for n in range(n_iterations):
        iters[n+1, :] = g(iters[n, :])

    return iters
```
# interpol

## quad


```python
# Функция, которая принимает 3 точки для постройки функции полинома 2 степени и точку, для которой надо предсказать значение
def sq_interpolation(x, y, x_new, dtype):
    A = np.zeros([3, 3], dtype=dtype)
    Y = np.zeros(3)
    for i in range(3):
        x_ = x[i]
        A[i, :] = [1, x_, x_**2]
        Y[i] = y[i]
        
    coefs = np.linalg.solve(A, Y) # вычисление коэффициентов полинома
    return coefs[0] + coefs[1]*x_new + coefs[2]*x_new**2 # вычисления предсказанного значение и его возврат
```

```python
# Функция, которая принимает на вход ряд данных с пропусками и возвращает его после квадратичной интерполяции
# Умеет предсказывать данные для точки x_i в двух режимах:
#   Ориентируясь только на изначальные данные (int_type='by_old)
#   Ориентируясь также на данные, предсказанные для пропусков, прешествующих i-тому (int_type='by_all)
def do_sq_int(row, int_type, dtype):
    new_row = np.copy(row) # Создаю новый ряд, аналогичный старому, для записи высчитанных значений

    for i in range(len(row)):
        if np.isnan(row[i]): # Проверяю на пропуск
            temp_x, temp_y = [], [] # Создаю массивы, куда будут записываться ближайшие известные точки для дальнейшей передачи в функцию sq_interpolation()
            j = 1
            if int_type=='by_old':
                while len(temp_x)<3: # Проверяю на пригодность (известность) точки, шагая в обе стороны от неизвестной, пока не найду 3 точки, чтобы построить на них полином
                    if i-j>=0:
                        prev_j = row[i-j]
                        if not np.isnan(prev_j):
                            temp_x.append(i-j)
                            temp_y.append(prev_j)
                    
                    if len(temp_x)==3: break
                    
                    if i+j<len(row):
                        next_j = row[i+j]
                        if not np.isnan(next_j):
                            temp_x.append(i+j)
                            temp_y.append(next_j)
                        
                    j+=1
                    
            if int_type=='by_all':
                while len(temp_x)<3: # Вариант, где учитываются и ранее предсказанные значения
                    if i-j>=0:
                        prev_j = new_row[i-j]
                        if not np.isnan(prev_j):
                            temp_x.append(i-j)
                            temp_y.append(prev_j)
                    
                    if len(temp_x)==3: break
                    
                    if i+j<len(row):
                        next_j = new_row[i+j]
                        if not np.isnan(next_j):
                            temp_x.append(i+j)
                            temp_y.append(next_j)
                        
                    j+=1
                    
            new_row[i] = sq_interpolation(temp_x, temp_y, i, dtype) # Заполняю пропуск
            
    return new_row
```
## spline


```python
def cubic_spline_coeff(x, y):
    n = len(x) - 1
    h = np.diff(x)
    
    A = np.zeros((4*n, 4*n))
    b = np.zeros(4*n)
    
    row = 0
    for i in range(n):
        A[row, 4*i:4*(i+1)] = [x[i]**3, x[i]**2, x[i], 1]
        b[row] = y[i]
        row += 1
        
        A[row, 4*i:4*(i+1)] = [x[i+1]**3, x[i+1]**2, x[i+1], 1]
        b[row] = y[i+1]
        row += 1
        
    for i in range(n-1):
        A[row, 4*i:4*(i+1)] = [3*x[i+1]**2, 2*x[i+1], 1, 0]
        A[row, 4*(i+1):4*(i+2)] = [-3*x[i+1]**2, -2*x[i+1], -1, 0]
        b[row] = 0
        row += 1
    
    for i in range(n-1):
        A[row, 4*i:4*(i+1)] = [6*x[i+1], 2, 0, 0]
        A[row, 4*(i+1):4*(i+2)] = [-6*x[i+1], -2, 0, 0]
        b[row] = 0
        row +=  1
        
    A[row, 4*(n-1):4*n] = [6*x[n], 2, 0, 0]
    b[row] = 0
    row += 1
    
    A[row, 0:4] = [6*x[0], 2, 0, 0]
    b[row] = 0
    print(A)
    coeffs = np.linalg.solve(A, b)
    coeffs = coeffs.reshape(n, 4)
    return coeffs
```

```python
def do_cubic_spline_int(coeffs, x_knwon, x_new):
    '''
    :param: x_known: те же x, что использовал для получения коэффициентов
    '''
    for i in range(len(x_knwon)-1):
        if x_knwon[i] <= x_new <= x_knwon[i+1]:
            a, b, c, d = coeffs[i]
            return a*x_new**3 + b*x_new**2 + c*x_new + d
        
    return None
```
# matmul

## naive


```python
# Наивный метод перемножения матриц
@jit(nopython=True)
def naive_method(A, B):
    n = A.shape[0]
    k = A.shape[1]
    m = B.shape[1]
    C = np.zeros((n, m))
    
    for i in range(n):
        for j in range(m):
            for s in range(k):
                C[i, j] += A[i, s]*B[s, j]
                
    return C
```
## strassen


```python
# Тот самый алгоритм Штрассена. Рекурсивно делю на 4 части и перемножаю матрицы по алгоритму:
@njit(nopython=True, parallel=True)
def strassen_mult(A, B):
    # Если на вход поступило 2 числа - возвращаем... число!
    if len(A)==1:
        return (A*B).astype(np.float64)
    
    n = A.shape[0]
    half = n//2
    
    A11 = A[:half, :half]
    A12 = A[:half, half:]
    A21 = A[half:, :half]
    A22 = A[half:, half:]
    
    B11 = B[:half, :half]
    B12 = B[:half, half:]
    B21 = B[half:, :half]
    B22 = B[half:, half:]
    
    F1 = strassen_mult(A11 + A22, B11 + B22)
    F2 = strassen_mult(A21 + A22, B11)
    F3 = strassen_mult(A11, B12 - B22)
    F4 = strassen_mult(A22, B21 - B11)
    F5 = strassen_mult(A11 + A12, B22)
    F6 = strassen_mult(A21 - A11, B11 + B12)
    F7 = strassen_mult(A12 - A22, B21 + B22)
    
    C = np.zeros(shape=(n, n))
    C[:half, :half] = F1 + F4 - F5 + F7
    C[:half, half:] = F3 + F5
    C[half:, :half] = F2 + F4
    C[half:, half:] = F1 - F2 + F3 + F6

    return C
```

```python
# Вспомогательаня функция, чтобы решать проблему размера матрицы n x n не вида n = 2^d:
def strassen_method(A, B):
    n1, m1 = A.shape
    n2, m2 = B.shape
    nn = max([n1, m1, n2, m2])

    # Если размер не является степенью двойки, добиваем строками/столбцами нулей
    if int(np.log2(nn)) != np.log2(nn) or (n1 != m1) or (n2 != m2):
        n_new = int(np.power(2, np.ceil(np.log2(nn))))
        A_new = np.zeros((n_new, n_new))
        B_new = np.zeros((n_new, n_new))
        A_new[:n1, :m1] = A
        B_new[:n2, :m2] = B
        
        C_new = strassen_mult(A_new, B_new)
        return C_new[:n1, :m2] # А вовзращаем матрицу такой, какой она должна была быть - без нулей
    
    # Иначе просто перемножаем
    C = strassen_mult(A, B)
    return C
```
# eigen


```python
def X_cov(X_centered, method):
    return method(X_centered.T, X_centered) / (height-1)
```
## power method


```python
def power_method(A, max_iters=100, tol=1e-4):
    n = A.shape[0]
    x0 = np.ones((n, 1))
    V = np.zeros((max_iters, n, 1))
    V[0, :] = x0
    lmds = np.zeros(max_iters)
    
    for i in range(max_iters-1):
        x_ = np.dot(A, V[i, :])
        x_ = x_ / np.max(x_)
        V[i+1, :] = x_
        lmds[i+1] = (V[i+1].T @ A @ V[i+1]) / (V[i+1].T @ V[i+1])
        if abs(lmds[i+1]-lmds[i])<tol and i>0:
            return lmds[:i+2], V[:i+2]
    
    return lmds, V
```
## jacobi


```python
# Вспомогательная функция - ищет наибольший по модулю элемент в треугольнике над главной диагональю, возвращает его и его координаты
def mx(A, p=0):
    n = A.shape[0]
    # Тестовый параметр - при p==1 ищем не только в верхнем, но и в нижнем треугольнике!
    if p==1:
        A_ = A - np.diag(np.diag(A))
        am = np.argmax(A_)
        i_m, j_m = am//n, am%n
        return A_[i_m, j_m], i_m, j_m
        
    a_m = 0
    i_m, j_m = 0, 0
    for i in range(0, n):
        for j in range(i+1, n):
            if np.abs(A[i, j]) > np.abs(a_m):
                a_m = A[i, j]
                i_m, j_m = i, j
    
    return a_m, i_m, j_m
```

```python
# Метод вращений
def jacobi_method(A, max_iters=100, tol=1e-4):
    # Выделяем память
    n = A.shape[0]
    vecs = np.eye(n, dtype=np.float64)
    A_k = np.zeros_like(A, dtype=np.float64)
    A_k[:, :] = A
    
    for k in range(max_iters):
        # Получаем максимальный по модулю недиагональный элемент, его координаты
        a_ij, i, j = mx(A_k, 0)
        
        # Делаем break, если матрица достаточно близка к диагональной
        if abs(a_ij) < tol:
            print(f'tolerance reached! (k = {k+1})')
            break
        
        # Вычисляем угол поворота phi
        a_ii, a_jj = A_k[i, i], A_k[j, j]
        phi = np.arctan((2 * a_ij) / (a_ii - a_jj)) / 2 if a_ii!=a_jj else np.pi/4
        
        # Создаём поворотную матрицу
        H_k = np.eye(n, dtype=np.float64)
        H_k[i, i] = np.cos(phi)
        H_k[i, j] = -np.sin(phi)
        H_k[j, i] = np.sin(phi)
        H_k[j, j] = np.cos(phi)
        # Обновляем матрицу собственных векторов
        vecs = np.dot(vecs, H_k)

        # Обновляем матрицу
        A_k = H_k.T @ A_k @ H_k
    else:
        print('max iters reached!')
    
    # Собственные значения - диагональ матрицы
    vals = np.diag(A_k)
        
    return vals, vecs
```
## householder for hessenberg


```python
# Привежение к верхнегессенберговской форме методом отражений Хаусхолдера
def householder_hessenberg(A, mm_method=np.dot, dtype=np.float32):
    n = A.shape[0]
    A_ = np.zeros_like(A, dtype=dtype)
    A_[:, :] = A
    Q = np.eye(n, dtype=dtype)
    
    for k in tqdm(range(n-2)):
        # Берём подстолбец k-ого столбца
        a = A_[k+1:, k]
        a_norm = norm(a)
        
        # Считаем матрицу отражения
        e1 = np.zeros_like(a, dtype=dtype)
        e1[0] = 1
        sign = np.sign(a[0])
        v = a + e1*sign*a_norm
        v = v / norm(v)
        
        P = np.eye(n-k-1) - 2*np.outer(v, v)
        H_k = np.eye(n, dtype=dtype)
        H_k[k+1:, k+1:] = P
        
        # Обновляем исходную матрицу и матрицу накопления преобразований Q
        A_[:, :] = mm_method(mm_method(H_k, A_), H_k)
        Q[:, :] = mm_method(Q, H_k)
        
    H = mm_method(mm_method(Q.T, A), Q).astype(dtype)
        
    return Q, H
```
## QR разл


```python
# QR-разложения методом отражений Хаусхолдера
def householder_QR(A, mm_method=np.dot, dtype=np.float32):
    n = A.shape[0]
    A_ = np.zeros_like(A, dtype=dtype)
    A_[:, :] = A
    Q = np.eye(n, dtype=dtype)
    
    for k in range(n):
        # Берём подстолбец матрицы
        a = A_[k:, k]
        a_norm = norm(a)
        
        # Получаем матрицу отражения H_k
        e1 = np.zeros_like(a, dtype=dtype)
        e1[0] = 1
        sign = np.sign(a[0])
        v = a + e1*sign*a_norm
        v = v / norm(v)
        
        P = np.eye(n-k) - 2*np.outer(v, v)
        H_k = np.eye(n, dtype=dtype)
        H_k[k:, k:] = P
        
        # Обновляем исходную матрицу и матрицу преобразований Q
        A_[:, :] = mm_method(H_k, A_)
        Q[:, :] = mm_method(Q, H_k)
        
    R = mm_method(Q.T, A).astype(dtype)
        
    return Q, R
```
## QR method


```python
# QR-алгоритм для приведение к верхнетреугольному виду, с собственными значениями на главной диагонали
def QR_algorithm(A, mm_method=np.dot, max_iters=100, dtype=np.float32):
    A_ = np.zeros_like(A, dtype=dtype)
    A_[:, :] = A
    
    for i in tqdm(range(max_iters)):
        # При stupid=True использует метод qr из np.linalg
        Q, R = householder_QR(A_, mm_method=mm_method)
        # A_(k+1) = R_k @ Q_k
        A_[:, :] = mm_method(R, Q)
        
    return A_
```
## back_iters


```python
# Метод обратной итерации с адаптивным выбором параметра сдвига при помощи отношентия Релея для ОДНОГО собственного значения
def back_iters_(A, lmd, mm_method=np.dot, max_iters=100, dtype=np.float32, tol=1e-6):
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / norm(v)
    
    for k in range(max_iters):
        # Сдвинутая матрица
        A_ = A - lmd*np.eye(n)
        # Вычисляем x_(k+1)
        try:
            x_k = mm_method(np.linalg.inv(A_), v)
        except np.linalg.LinAlgError:
            A_ = A_ + np.eye(n)*1e-6
            x_k = mm_method(np.linalg.inv(A_), v)
            
        # Новое приблежение собственного вектора
        v_new = x_k / norm(x_k)
        # Новое приближение собственного значения
        lmd_new = (mm_method(mm_method(v_new, A), v_new[:, np.newaxis]) / mm_method(v_new, v_new))[0]
        
        # Проверяем сходимость
        if norm(v_new - v) < tol and np.abs(lmd_new - lmd) < tol:
            break
        
        v = v_new
        lmd = lmd_new
        
    return lmd, v
    

# Метод обратной итерации для ВСЕХ собственных значений (приближения берём из диагонали матрицы R - результата QR-алгоритма)
def back_iters(A, R, mm_method=np.dot, max_iters=100, dtype=np.float32, tol=1e-3, cnt=None):
    mm_method = np.dot
    n = A.shape[0]
    if cnt is None: cnt = n
    Lmd = np.diag(R)
    srt = np.abs(Lmd).argsort()[::-1]
    # первые приближения
    eigen_values = Lmd.copy().astype(dtype)[srt]
    eigen_vectors = np.zeros_like(A, dtype=dtype)
    
    for i in tqdm(range(cnt)):
        lmd, v = back_iters_(A, eigen_values[i], mm_method=mm_method, max_iters=max_iters, dtype=dtype, tol=tol)
        eigen_values[i] = lmd
        eigen_vectors[:, i] = v
            
    return eigen_values, eigen_vectors
```
# difur

## прям


```python
h = np.logspace(-7, 1)
fd_estimate = (np.exp(h) - np.exp(0.0)) / h
err = np.abs(fd_estimate - 1.0)
```
## центр


```python
h = np.logspace(-5, 1)
fd_estimate = (np.exp(h) - np.exp(-h)) / (2*h)
err = np.abs(fd_estimate - 1.0)
```
## euler


```python
def euler_method(f, x_end, y0, N):
    h = x_end/N
    x = np.linspace(0.0, x_end, N+1)
    y = np.zeros((N+1, len(y0)))
    y[0, :] = y0
    for n in range(N):
        y[n+1, :] = y[n, :] + h*f(x[n], y[n, :])
        
    return x, y
```
## euler pc


```python
def euler_pc_method(f, x_end, y0, N):
    h = x_end/N
    x = np.linspace(0.0, x_end, N+1)
    y = np.zeros((N+1, len(y0)))
    y[0, :] = y0
    
    for n in range(N):
        fn = f(x[n], y[n])
        yp = y[n] + h * fn
        y[n+1, :] = y[n, :] + h/2 * (fn + f(x[n+1], yp))
        
    return x, y
```
# fourier

## dft


```python
def dft(x):
    N = len(x)
    # Результат в виде массива комплексных чисел
    X = np.zeros_like(x, dtype=complex)
    
    for k in range(N):
        sum_r = 0.0
        sum_i = 0.0
        for n in range(N):
            angle = -2 * np.pi * k * n / N
            r = np.cos(angle)
            i = np.sin(angle)
            sum_r += x[n] * r
            sum_i += x[n] * i
        X[k] = complex(sum_r, sum_i)
    
    return X
```
## idft


```python
def idft(X):
    N = len(X)
    # Результат востановления
    x = np.zeros_like(X, dtype=float)

    for n in range(N):
        sum_r = 0.0
        for k in range(N):
            angle = 2 * np.pi * k * n / N
            r = np.cos(angle)
            i = np.sin(angle)
            sum_r += X[k].real * r - X[k].imag * i
        x[n] = sum_r / N

    return x
```

```python

```
