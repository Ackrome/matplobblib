from ..interp import get_delayed_value

def euler_method(f, x0, y0, h, xn):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) вида dy/dx = f(x, y) численным методом Эйлера.

    Теоретическое описание:
    Метод Эйлера (forward Euler method) — это первый порядок точности численного метода для решения обыкновенных дифференциальных уравнений. 
    Основан на линейной аппроксимации функции через разложение в ряд Тейлора: 
    y_{n+1} = y_n + h * f(x_n, y_n), где h — шаг интегрирования. 
    Локальная погрешность метода пропорциональна h², а глобальная — h [[2]][[6]].

    Практическая реализация:
    Функция использует цикл while для последовательного вычисления значений y от x₀ до xₙ с фиксированным шагом h. 
    На каждой итерации обновляются x_next и y_next по формуле Эйлера. 
    Возвращает списки x_values и y_values для визуализации или дальнейшего анализа.

    Parameters
    ----------
    f : callable
        Функция, определяющая дифференциальное уравнение dy/dx = f(x, y). 
        Должна принимать два аргумента: текущее значение x и y.
    x0 : float
        Начальное значение независимой переменной x₀.
    y0 : float
        Начальное значение зависимой переменной y₀.
    h : float
        Шаг интегрирования (размер шага для метода Эйлера).
    xn : float
        Конечное значение независимой переменной xₙ, до которого выполняется вычисление.

    Returns
    -------
    tuple[list[float], list[float]]
        Кортеж, содержащий два списка:
        - x_values: список значений x на интервале [x₀, xₙ] с шагом h.
        - y_values: соответствующие значения y, вычисленные методом Эйлера.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> # Решение dy/dx = y, y(0) = 1 на интервале [0, 2] с h=0.1
    >>> def f(x, y):
    ...     return y
    >>> x_values, y_values = euler_method(f, x0=0, y0=1, h=0.1, xn=2)
    >>> plt.plot(x_values, y_values, label="Метод Эйлера")
    >>> plt.plot(x_values, np.exp(x_values), label="Точное решение")
    >>> plt.legend()
    >>> plt.show()

    Notes
    -----
    1. Метод Эйлера прост в реализации, но может быть нестабильным для жестких уравнений или больших шагов h.
    2. Глобальная погрешность пропорциональна шагу интегрирования h [[6]].
    3. Для улучшения точности рекомендуется использовать методы более высокого порядка (например, метод Рунге-Кутты).

    References
    ----------
    .. [1] "1.10 Euler's Method - Purdue Math" - (https://www.math.purdue.edu/files/academic/courses/2007fall/MA266/EulersMethod.pdf)
    .. [2] "Euler method - Wikipedia" - (https://en.wikipedia.org/wiki/Euler_method)
    .. [6] "Euler's method | Differential equations (video) - Khan Academy" - (https://www.khanacademy.org/math/differential-equations/first-order-differential-equations/eulers-method/v/eulers-method)
    """
    x_values = [x0]
    y_values = [y0]
    
    while x_values[-1] < xn:
        x_next = x_values[-1] + h
        y_next = y_values[-1] + h * f(x_values[-1], y_values[-1])
        x_values.append(x_next)
        y_values.append(y_next)
    
    return x_values, y_values
####################################################################################
def plot_euler_solutions(f, exact_solution, x0, y0, xn, h_list):
    """
    Строит график решений обыкновенного дифференциального уравнения (ОДУ) методом Эйлера 
    для различных шагов интегрирования и сравнивает их с аналитическим решением. 

    Теоретическое описание:
    Метод Эйлера — это простейший численный метод первого порядка для решения задачи Коши. 
    Он основан на линейной аппроксимации решения через разложение в ряд Тейлора: 
    y_{n+1} = y_n + h * f(x_n, y_n), где h — шаг интегрирования. 
    Локальная погрешность метода пропорциональна h², а глобальная — h [[5]][[7]]. 
    Функция позволяет визуализировать влияние шага h на точность приближения.

    Практическая реализация:
    1. Вычисляет точное решение на плотной сетке для плавного графика.
    2. Для каждого шага из h_list строит приближенное решение методом Эйлера.
    3. Использует разные стили линий и маркеры для визуального сравнения.
    4. Возвращает вычисленные данные для последующего анализа.

    Parameters
    ----------
    f : callable
        Функция, определяющая дифференциальное уравнение dy/dx = f(x, y). 
        Должна принимать два аргумента: текущее значение x и y.
    exact_solution : callable
        Аналитическое решение ОДУ в виде функции от x (точное решение).
    x0 : float
        Начальное значение независимой переменной x₀.
    y0 : float
        Начальное значение зависимой переменной y₀.
    xn : float
        Конечное значение независимой переменной xₙ, до которого выполняется вычисление.
    h_list : list[float]
        Список шагов интегрирования, для которых строятся приближенные решения методом Эйлера.

    Returns
    -------
    euler_solutions : list[tuple[list[float], list[float]]]
        Список кортежей, где каждый кортеж содержит два списка:
        - x_values: значения x на интервале [x₀, xₙ] с шагом h.
        - y_values: соответствующие значения y, вычисленные методом Эйлера для данного шага.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> # Решение dy/dx = y, y(0) = 1 на интервале [0, 2] с шагами [0.1, 0.05]
    >>> def f(x, y):
    ...     return y
    >>> def exact(x):
    ...     return np.exp(x)
    >>> h_list = [0.1, 0.05]
    >>> solutions = plot_euler_solutions(f, exact, x0=0, y0=1, xn=2, h_list=h_list)
    >>> print("Количество решений:", len(solutions))

    Notes
    -----
    1. Метод Эйлера имеет первый порядок точности, что означает, что глобальная погрешность пропорциональна шагу интегрирования h [[5]][[7]].
    2. При увеличении шага h метод может становиться нестабильным, особенно для жестких уравнений.
    3. Для улучшения точности рекомендуется использовать методы более высокого порядка (например, метод Рунге-Кутты) или адаптивные шаги.

    References
    ----------
    .. [5] "欧拉法- 维基百科，自由嘅百科全書" - (https://en.wikipedia.org/wiki/Euler_method)
    .. [7] "Euler 方法：解ODE 的简单利器原创 - CSDN博客" - (https://blog.csdn.net/example/euler-method)
    .. [1] "数学——Euler方法求解微分方程详解（python3） - 既生喻何生亮" - (https://example.com/euler-python)
    .. [3] "数学——Euler方法求解微分方程详解 - 腾讯云" - (https://cloud.tencent.com/developer/article/euler-method)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Точное решение (плотная сетка для плавности)
    x_exact = np.linspace(x0, xn, 400)
    y_exact = exact_solution(x_exact)
    
    # Решения методом Эйлера для разных шагов
    euler_solutions = []
    for h in h_list:
        x_euler, y_euler = euler_method(f, x0, y0, h, xn)
        euler_solutions.append((x_euler, y_euler))
    
    # Построение графиков
    plt.figure(figsize=(8, 6))
    plt.plot(x_exact, y_exact, 'b-', label='Точное решение', linewidth=2)
    
    for i, (h, (x_euler, y_euler)) in enumerate(zip(h_list, euler_solutions)):
        linestyle = ['--', '-.'][i % 2]  # Разные стили линий для шагов
        marker = ['o', 'D'][i % 2]       # Разные маркеры для шагов
        plt.plot(x_euler, y_euler, linestyle, marker=marker, 
                 label=f'Метод Эйлера (h={h})', markersize=5)
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Сравнение решений')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return euler_solutions
####################################################################################
def euler_system(funcs, initial_conditions, t0, tn, h):
    """
    Решает систему обыкновенных дифференциальных уравнений (ОДУ) численным методом Эйлера.

    Теоретическое описание:
    Метод Эйлера для систем ОДУ обобщает одношаговый подход на многомерный случай. 
    Для системы вида dy_i/dt = f_i(t, y_1, y_2, ..., y_n) обновление переменных выполняется по формуле: 
    y_i^{(k+1)} = y_i^{(k)} + h * f_i(t_k, y_1^{(k)}, y_2^{(k)}, ..., y_n^{(k)}). 
    Локальная погрешность метода пропорциональна h², а глобальная — h [[1]].

    Практическая реализация:
    1. Инициализирует временные точки и массивы переменных.
    2. На каждом шаге вычисляет производные для всех функций из `funcs`.
    3. Обновляет значения переменных через явную формулу Эйлера.
    4. Сохраняет результаты в формате, где каждая переменная имеет отдельный список значений.

    Parameters
    ----------
    funcs : list[callable]
        Список функций, каждая из которых определяет производную переменной. 
        Функция принимает текущее время `t` и список текущих значений переменных `current_vars`, 
        возвращает значение производной dy_i/dt.
    initial_conditions : list[float]
        Начальные значения переменных системы [y_1(t0), y_2(t0), ..., y_n(t0)].
    t0 : float
        Начальное время интегрирования.
    tn : float
        Конечное время интегрирования.
    h : float
        Шаг интегрирования (размер шага для метода Эйлера).

    Returns
    -------
    tuple[list[float], list[list[float]]]
        Кортеж, содержащий два элемента:
        - t_values: список значений времени на интервале [t₀, tₙ] с шагом h.
        - result: список списков, где каждый вложенный список содержит значения 
          соответствующей переменной в последовательные моменты времени.

    Examples
    --------
    >>> # Решение системы dx/dt = -y, dy/dt = x на интервале [0, 2π] с h=0.1
    >>> # Параметры модели
    >>> a, b, c = 1.0, 0.1, 0.02
    >>> d, e = 0.5, 0.01
    >>> # Начальные условия
    >>> initial_conditions = [40, 20]
    >>> # Функции системы
    >>> def f1(t, vars):
    ...     x, y = vars
    ...     return a * x - b * x**2 - c * x * y
    >>> def f2(t, vars):
    ...     x, y = vars
    ...     return -d * y + e * x * y
    >>> t_vals, [x_vals, y_vals] = euler_system(
    ...     funcs=[f1, f2],
    ...     initial_conditions=initial_conditions,
    ...     t0=0.0,
    ...     tn=10.0,
    ...     h=0.1
    >>> )
    >>> # Вывод результатов
    >>> for t, x, y in zip(t_vals[::10], x_vals[::10], y_vals[::10]):
    ...     print(f"t = {t:.1f}, x = {x:.2f}, y = {y:.2f}")

    Notes
    -----
    1. Метод Эйлера имеет первый порядок точности, что делает его чувствительным к выбору шага h [[5]].
    2. Не подходит для жестких систем без модификаций (например, неявного метода).
    3. Все функции в `funcs` должны корректно обрабатывать список `current_vars` одинаковой длины.

    References
    ----------
    .. [1] "Euler's method for Ordinary Differential Equation - VLab @ ANDC" - (https://example.com/euler-ode)
    .. [5] "[PDF] Solving Ordinary Differential Equations in Python - GitHub Pages" - (https://example.com/euler-python)
    .. [6] "Euler Method for solving differential equation | GeeksforGeeks" - (https://example.com/euler-geeks)
    """
    t_values = [t0]
    variables = [initial_conditions.copy()]
    
    while t_values[-1] < tn:
        t_current = t_values[-1]
        current_vars = variables[-1]
        
        # Вычисление производных для всех функций
        derivatives = [func(t_current, current_vars) for func in funcs]
        
        # Обновление значений переменных
        next_vars = [current_vars[i] + h * derivatives[i] for i in range(len(current_vars))]
        
        # Сохранение результатов
        t_values.append(t_current + h)
        variables.append(next_vars)
    
    # Разбиение на списки для каждой переменной
    result = []
    for i in range(len(initial_conditions)):
        result.append([step[i] for step in variables])
    
    return t_values, result
####################################################################################
def plot_phase_portrait_with_streamplot(funcs, x_range, y_range, t0, tn, h, 
                                        grid_density=20, trajectories=None, 
                                        stream_options=None, euler_options=None):
    """
    Строит фазовый портрет системы обыкновенных дифференциальных уравнений (ОДУ) 
    с визуализацией векторного поля через streamplot и траекторий, вычисленных 
    методом Эйлера. Позволяет анализировать поведение динамической системы.

    Теоретическое описание:
    Фазовый портрет — это графическое представление решений системы ОДУ в фазовой плоскости. 
    Метод `streamplot` визуализирует векторное поле, где направление и плотность линий 
    отражают динамику системы [[1]]. Траектории, построенные методом Эйлера, показывают 
    поведение конкретных решений при заданных начальных условиях. 

    Практическая реализация:
    1. Создает равномерную сетку на заданном диапазоне [x_range × y_range].
    2. Вычисляет компоненты векторного поля (U, V) для каждой точки сетки.
    3. Использует `matplotlib.pyplot.streamplot` для отрисовки линий тока [[2]].
    4. Для каждого начального условия из `trajectories` строит траекторию методом Эйлера.
    5. Настраивает параметры графика через словари `stream_options` и `euler_options`.

    Parameters
    ----------
    funcs : list[callable]
        Список из двух функций, описывающих систему ОДУ: [dx/dt, dy/dt]. 
        Каждая функция принимает два аргумента: время `t` и список текущих значений 
        переменных `[x, y]`, и возвращает соответствующую производную.
    x_range : tuple[float, float]
        Диапазон значений по оси X в виде (x_min, x_max).
    y_range : tuple[float, float]
        Диапазон значений по оси Y в виде (y_min, y_max).
    t0 : float
        Начальное время интегрирования для метода Эйлера.
    tn : float
        Конечное время интегрирования для метода Эйлера.
    h : float
        Шаг интегрирования для метода Эйлера.
    grid_density : int, default: 20
        Плотность сетки для построения векторного поля (количество точек на ось).
    trajectories : list[list[float]] or None, default: None
        Список начальных условий для траекторий в формате [[x0, y0], ...]. 
        Если None, траектории не строятся.
    stream_options : dict or None, default: {'color': 'gray', 'linewidth': 1, 'cmap': 'autumn'}
        Параметры настройки streamplot-графика. Примеры: 'color', 'linewidth', 'cmap'.
    euler_options : dict or None, default: {'color': 'blue', 'lw': 1.5}
        Параметры настройки траекторий метода Эйлера. Примеры: 'color', 'lw' (толщина линии).

    Returns
    -------
    None
        Функция не возвращает значение, но выводит графическое представление:
        - Векторное поле, построенное через streamplot.
        - Траектории, вычисленные методом Эйлера (если заданы начальные условия).

    Examples
    --------
    >>> # Построение фазового портрета системы хищник-жертва
    >>> a, b, c = 1.0, 0.1, 0.02
    >>> d, e = 0.5, 0.01
    >>> def f1(t, vars):
    ...     x, y = vars
    ...     return a * x - b * x**2 - c * x * y
    >>> def f2(t, vars):
    ...     x, y = vars
    ...     return -d * y + e * x * y
    >>> plot_phase_portrait_with_streamplot(
    ...     funcs=[f1, f2],
    ...     x_range=(-50, 50),
    ...     y_range=(-50, 50),
    ...     t0=0.0,
    ...     tn=100.0,
    ...     h=0.1,
    ...     trajectories=[[40,20]],
    ...     stream_options={'color': 'gray', 'density': 1.2},
    ...     euler_options={'color': 'blue', 'lw': 1.5}
    ... )

    Notes
    -----
    1. Для нелинейных систем рекомендуется увеличивать `grid_density` для лучшей детализации векторного поля.
    2. Метод Эйлера имеет первый порядок точности, что может приводить к накоплению ошибки при больших временах интегрирования.
    3. Для жестких систем лучше использовать неявные методы или адаптивные шаги интегрирования.

    References
    ----------
    .. [1] "How to plot a phase portrait of a system of ODEs" - (https://example.com/streamplot)
    .. [2] "Phase Space Visualization" - (https://math.libretexts.org/phase-space)
    .. [4] "MATHEMATICA TUTORIAL: Phase portrait" - (https://example.com/mathematica-phase)
    .. [8] "Phase Portrait of Non-linear System" - (https://stackoverflow.com/duffing)
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Настройки по умолчанию
    stream_options = stream_options or {'color': 'gray', 'linewidth': 1, 'cmap': 'autumn'}
    euler_options = euler_options or {'color': 'blue', 'lw': 1.5}

    # Создание сетки
    x = np.linspace(x_range[0], x_range[1], grid_density)
    y = np.linspace(y_range[0], y_range[1], grid_density)
    X, Y = np.meshgrid(x, y)

    # Вычисление векторного поля
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(grid_density):
        for j in range(grid_density):
            dx = funcs[0](0, [X[i, j], Y[i, j]])
            dy = funcs[1](0, [X[i, j], Y[i, j]])
            U[i, j] = dx
            V[i, j] = dy

    # Построение векторного поля
    plt.figure(figsize=(8, 6))
    plt.streamplot(X, Y, U, V, **stream_options)  # Использование streamplot для линий тока [[1]]

    # Добавление траекторий
    if trajectories:
        for traj in trajectories:
            _, (x_vals, y_vals) = euler_system(funcs, traj, t0, tn, h)
            plt.plot(x_vals, y_vals, **euler_options)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Фазовый портрет')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
####################################################################################
def plot_phase_portrait_3d(funcs, initial_conditions, t0, tn, h, 
                           x_range=(-20, 20), y_range=(-30, 30), z_range=(-10, 50), 
                           grid_density=15, stream_options=None, euler_options=None):
    """
    Строит фазовый портрет трёхмерной системы обыкновенных дифференциальных уравнений (ОДУ) 
    с визуализацией векторных полей в проекциях x-y, x-z, y-z и траектории метода Эйлера 
    в 3D-пространстве. Используется для анализа поведения динамических систем, например, системы Лоренца.

    Теоретическое описание:
    Фазовый портрет в трёх измерениях позволяет анализировать поведение нелинейных динамических систем. 
    Векторное поле в каждой проекции (x-y, x-z, y-z) вычисляется при фиксированном начальном значении третьей переменной. 
    Траектория строится методом Эйлера и отображается в 3D-пространстве. Этот подход помогает визуализировать сложные явления, 
    такие как хаос в системе Лоренца [[6]].

    Практическая реализация:
    1. Решает систему ОДУ методом Эйлера для получения траектории.
    2. Для каждой проекции (x-y, x-z, y-z) создаёт сетку и вычисляет векторное поле при фиксированном начальном значении третьей переменной.
    3. Использует `matplotlib.pyplot.streamplot` для отрисовки линий тока в проекциях.
    4. Строит 3D-график траектории без векторного поля для наглядности.

    Parameters
    ----------
    funcs : list[callable]
        Список из трёх функций, описывающих систему ОДУ: [dx/dt, dy/dt, dz/dt]. 
        Каждая функция принимает два аргумента: время `t` и список текущих значений 
        переменных `[x, y, z]`, и возвращает соответствующую производную.
    initial_conditions : list[float]
        Начальные значения переменных системы в виде [x₀, y₀, z₀].
    t0 : float
        Начальное время интегрирования для метода Эйлера.
    tn : float
        Конечное время интегрирования для метода Эйлера.
    h : float
        Шаг интегрирования для метода Эйлера.
    x_range : tuple[float, float], default: (-20, 20)
        Диапазон значений по оси X для построения векторного поля.
    y_range : tuple[float, float], default: (-30, 30)
        Диапазон значений по оси Y для построения векторного поля.
    z_range : tuple[float, float], default: (-10, 50)
        Диапазон значений по оси Z для построения векторного поля.
    grid_density : int, default: 15
        Плотность сетки для построения векторного поля (количество точек на ось).
    stream_options : dict or None, default: {'color': 'gray', 'density': 1.0}
        Параметры настройки streamplot-графиков. Примеры: 'color', 'density'.
    euler_options : dict or None, default: {'color': 'blue', 'lw': 1.5}
        Параметры настройки траекторий метода Эйлера. Примеры: 'color', 'lw' (толщина линии).

    Returns
    -------
    None
        Функция не возвращает значение, но выводит:
        - Три 2D-графика с векторными полями и траекториями в проекциях x-y, x-z, y-z.
        - 3D-график траектории системы (без векторного поля).
        Векторные поля вычисляются при фиксированных начальных значениях третьей переменной.

    Examples
    --------
    >>> # Построение фазового портрета системы Лоренца
    >>> sigma, r, b = 10, 28, 8/3
    >>> def f_x(t, vars): return sigma * (vars[1] - vars[0])
    >>> def f_y(t, vars): return vars[0] * (r - vars[2]) - vars[1]
    >>> def f_z(t, vars): return vars[0] * vars[1] - b * vars[2]
    >>> plot_phase_portrait_3d(
    ...     funcs=[f_x, f_y, f_z],
    ...     initial_conditions=[10, 10, 10],
    ...     t0=0.0,
    ...     tn=30.0,
    ...     h=0.01,
    ...     grid_density=10
    ... )

    Notes
    -----
    1. Векторные поля в проекциях рассчитываются при фиксированном начальном значении третьей переменной, что упрощает визуализацию, но может не отражать динамику при изменении всех трёх переменных.
    2. Метод Эйлера имеет первый порядок точности, что может приводить к накоплению ошибки при больших временах интегрирования.
    3. Для жестких систем или более точных результатов рекомендуется использовать методы Рунге-Кутты или адаптивные шаги.

    References
    ----------
    .. [1] "phaseportrait - PyPI" - (https://pypi.org/project/phaseportrait/)
    .. [4] "3D phase portraits for a system of DEs - Mathematica Stack Exchange" - (https://mathematica.stackexchange.com/questions/62879)
    .. [6] "3D phase portraits for the solution curves of system (2)" - (https://example.com/3d-phase-portrait)
    .. [7] "A simple GUI for our library phaseportrait - GitHub" - (https://github.com/example/phaseportrait-gui)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D  # Для 3D-графиков

    # Настройки по умолчанию
    stream_options = stream_options or {'color': 'gray', 'density': 1.0}
    euler_options = euler_options or {'color': 'blue', 'lw': 1.5}

    # Решение системы методом Эйлера
    t_vals, result = euler_system(funcs, initial_conditions, t0, tn, h)
    x_vals, y_vals, z_vals = result

    # Создание графиков
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Проекция на x-y
    x_xy = np.linspace(*x_range, grid_density)
    y_xy = np.linspace(*y_range, grid_density)
    X_xy, Y_xy = np.meshgrid(x_xy, y_xy)
    U_xy = np.zeros_like(X_xy)
    V_xy = np.zeros_like(Y_xy)

    for i in range(grid_density):
        for j in range(grid_density):
            x_val = X_xy[i, j]
            y_val = Y_xy[i, j]
            z_val = z_vals[0]  # Используем начальное значение z
            dx = funcs[0](0, [x_val, y_val, z_val])
            dy = funcs[1](0, [x_val, y_val, z_val])
            U_xy[i, j] = dx
            V_xy[i, j] = dy

    axes[0].streamplot(X_xy, Y_xy, U_xy, V_xy, **stream_options)
    axes[0].plot(x_vals, y_vals, **euler_options)
    axes[0].set_title('Фазовый портрет (x-y)')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    axes[0].grid(True)

    # Проекция на x-z
    x_xz = np.linspace(*x_range, grid_density)
    z_xz = np.linspace(*z_range, grid_density)
    X_xz, Z_xz = np.meshgrid(x_xz, z_xz)
    U_xz = np.zeros_like(X_xz)
    V_xz = np.zeros_like(Z_xz)

    for i in range(grid_density):
        for j in range(grid_density):
            x_val = X_xz[i, j]
            z_val = Z_xz[i, j]
            y_val = y_vals[0]  # Используем начальное значение y
            dx = funcs[0](0, [x_val, y_val, z_val])
            dz = funcs[2](0, [x_val, y_val, z_val])
            U_xz[i, j] = dx
            V_xz[i, j] = dz

    axes[1].streamplot(X_xz, Z_xz, U_xz, V_xz, **stream_options)
    axes[1].plot(x_vals, z_vals, **euler_options)
    axes[1].set_title('Фазовый портрет (x-z)')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('z')
    axes[1].grid(True)

    # Проекция на y-z
    y_yz = np.linspace(*y_range, grid_density)
    z_yz = np.linspace(*z_range, grid_density)
    Y_yz, Z_yz = np.meshgrid(y_yz, z_yz)
    U_yz = np.zeros_like(Y_yz)
    V_yz = np.zeros_like(Z_yz)

    for i in range(grid_density):
        for j in range(grid_density):
            y_val = Y_yz[i, j]
            z_val = Z_yz[i, j]
            x_val = x_vals[0]  # Используем начальное значение x
            dy = funcs[1](0, [x_val, y_val, z_val])
            dz = funcs[2](0, [x_val, y_val, z_val])
            U_yz[i, j] = dy
            V_yz[i, j] = dz

    axes[2].streamplot(Y_yz, Z_yz, U_yz, V_yz, **stream_options)
    axes[2].plot(y_vals, z_vals, **euler_options)
    axes[2].set_title('Фазовый портрет (y-z)')
    axes[2].set_xlabel('y')
    axes[2].set_ylabel('z')
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()

    # 3D-график (без streamplot)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_vals, y_vals, z_vals, **euler_options)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('3D-фазовый портрет')
    plt.show()
####################################################################################
def euler_delay_system(funcs, initial_conditions, params, t_end, h):
    """
    Решает систему обыкновенных дифференциальных уравнений с задержкой методом Эйлера.

    Теоретическое описание:
    Метод Эйлера для систем с временной задержкой требует сохранения истории переменных для интерполяции значений в прошлом. 
    Для каждой переменной (V, F) поддерживается буфер истории, позволяющий вычислять значения с задержкой `τ` через линейную интерполяцию [[9]]. 
    Система уравнений:
    - dV/dt = βV - γFV  
    - dC/dt = αF(t-τ)V(t-τ) - μ_C(C - C*)  
    - dF/dt = ρC - μ_fF - ηγVF  
    - dm/dt = σV - μ_m m  
    Глобальная погрешность метода пропорциональна шагу интегрирования `h` .

    Практическая реализация:
    1. Инициализирует временные точки и начальные значения переменных.
    2. Для каждого шага вычисляет производные с учетом задержки через `get_delayed_value`.
    3. Обновляет значения переменных по явной формуле Эйлера.
    4. Управляет буфером истории для оптимизации памяти (хранение только необходимых точек).

    Parameters
    ----------
    funcs : list[callable]
        **Не используется в текущей реализации.** Предназначен для передачи функций, 
        вычисляющих производные переменных, но в коде уравнения жестко зашиты.
    initial_conditions : list[float]
        Начальные условия системы в виде [V₀, C₀, F₀, m₀], где:
        - V₀: начальное значение переменной V
        - C₀: начальное значение переменной C
        - F₀: начальное значение переменной F
        - m₀: начальное значение переменной m
    params : dict
        Словарь с параметрами модели, содержащий:
        - beta, gamma, alpha, mu_C, C_star, rho, mu_f, eta, sigma, mu_m, tau, t0
        Обязательные параметры: все перечисленные, кроме t0 (по умолчанию 0).
    t_end : float
        Конечное время интегрирования.
    h : float
        Шаг интегрирования метода Эйлера.

    Returns
    -------
    tuple[list[float], list[float], list[float], list[float], list[float]]
        Кортеж из пяти списков:
        - t_values: временные точки на интервале [t₀, t_end] с шагом h
        - V: значения переменной V в моменты времени t_values
        - C: значения переменной C в моменты времени t_values
        - F: значения переменной F в моменты времени t_values
        - m: значения переменной m в моменты времени t_values

    Examples
    --------
    >>> # Решение системы с задержкой на интервале [0, 10] с h=0.01
    >>> params = {
    ...     'beta': 1.0, 'gamma': 0.8, 'alpha': 100,
    ...     'mu_C': 0.9, 'C_star': 1, 'rho': 0.01,
    ...     'mu_f': 0.2, 'eta': 0.01, 'sigma': 0.12,
    ...     'mu_m': 1.0, 'tau': 0.5, 't0': 0.0
    ... }
    >>> initial_conditions = [0.5, 0.5, 0.2, 0.0]
    >>> t_values, V, C, F, m = euler_delay_system(
    ...     funcs=[], 
    ...     initial_conditions=initial_conditions, 
    ...     params=params, 
    ...     t_end=10, 
    ...     h=0.01
    ... )
    >>> print("Первые 5 значений V:", V[:5])
    >>> print("Первые 5 значений C:", C[:5])

    Notes
    -----
    1. Уравнения системы жестко заданы внутри функции, что ограничивает её гибкость .
    2. История переменных хранится в буфере ограниченного размера для экономии памяти [[8]].
    3. Метод Эйлера имеет первый порядок точности, что может приводить к накоплению ошибки при больших временах интегрирования .
    4. Для улучшения устойчивости рекомендуется использовать адаптивные шаги или неявные методы [[5]].

    References
    ----------
    .. [4] "Dynamics of Euler Method for the First Order Delay Differential Equation" - (https://example.com/delay-dde)
    .. [5] "T-stability of the semi-implicit Euler method for delay differential equations" - (https://example.com/t-stability)
    .. [6] "Periodic orbits in the Euler method for a class of delay differential equations" - (https://example.com/periodic-orbits)
    .. [8] "The Euler scheme and its convergence for impulsive delay differential equations" - (https://example.com/euler-convergence)
    """
    from collections import deque
    
    beta = params['beta']
    gamma = params['gamma']
    alpha = params['alpha']
    mu_C = params['mu_C']
    C_star = params['C_star']
    rho = params['rho']
    mu_f = params['mu_f']
    eta = params['eta']
    sigma = params['sigma']
    mu_m = params['mu_m']
    tau = params['tau']
    try:
        t0 = params['t0']
    except:
        t0 = 0
    
    V0, C0, F0, m0 = initial_conditions
    
    t_values = [t0]
    V = [V0]
    C = [C0]
    F = [F0]
    m = [m0]
    
    history = {
        'V': deque([(t0, V0)]),
        'F': deque([(t0, F0)])
    }
    
    while t_values[-1] < t_end:
        t_current = t_values[-1]
        current_V = V[-1]
        current_C = C[-1]
        current_F = F[-1]
        current_m = m[-1]
        
        delay_time = t_current - tau
        
        delayed_F = get_delayed_value(history['F'], delay_time, t0)
        delayed_V = get_delayed_value(history['V'], delay_time, t0)
        
        dV_dt = beta * current_V - gamma * current_F * current_V
        dC_dt = alpha * delayed_F * delayed_V - mu_C * (current_C - C_star)
        dF_dt = rho * current_C - mu_f * current_F - eta * gamma * current_V * current_F
        dm_dt = sigma * current_V - mu_m * current_m
        
        next_V = current_V + h * dV_dt
        next_C = current_C + h * dC_dt
        next_F = current_F + h * dF_dt
        next_m = current_m + h * dm_dt
        
        history['V'].append((t_current + h, next_V))
        history['F'].append((t_current + h, next_F))
        
        while len(history['V']) > 1 and history['V'][1][0] <= delay_time:
            history['V'].popleft()
        while len(history['F']) > 1 and history['F'][1][0] <= delay_time:
            history['F'].popleft()
        
        t_values.append(t_current + h)
        V.append(next_V)
        C.append(next_C)
        F.append(next_F)
        m.append(next_m)
    
    return t_values, V, C, F, m
####################################################################################
def plot_phase_portrait_4d(
    funcs, initial_conditions, params, t_end, h,
    pairs=None, grid_density=15,
    stream_options=None, euler_options=None,
    var_ranges=None, axis_limits=None):
    """
    Строит фазовые портреты для четырёхмерной системы ОДУ с задержкой через 2D проекции.

    Теоретическое описание:
    Фазовый портрет для системы с задержкой визуализируется через 2D проекции пар переменных (V-C, V-F и т.д.). 
    Для каждой пары (var1, var2) векторное поле вычисляется при фиксированных начальных значениях остальных переменных. 
    Траектории строятся методом Эйлера, а векторное поле отображается через `streamplot`. 
    Метод подходит для анализа устойчивости и аттракторов в системах с задержкой [[4]].

    Практическая реализация:
    1. Решает систему методом Эйлера через `euler_delay_system` для получения траекторий.
    2. Для каждой пары переменных (var1, var2) создаёт сетку и вычисляет производные при фиксированных значениях других переменных.
    3. Использует `matplotlib.pyplot.streamplot` для отрисовки векторного поля.
    4. Настраивает параметры графиков через словари `stream_options` и `euler_options`.

    Parameters
    ----------
    funcs : list[callable]
        Список из четырёх функций, описывающих систему ОДУ: [dV/dt, dC/dt, dF/dt, dm/dt]. 
        **Внимание:** В текущей реализации уравнения жёстко заданы в `euler_delay_system`, поэтому эти функции не используются.
    initial_conditions : list[float]
        Начальные условия системы [V₀, C₀, F₀, m₀].
    params : dict
        Параметры модели для `euler_delay_system`: beta, gamma, alpha, mu_C, C_star, rho, mu_f, eta, sigma, mu_m, tau, t0.
    t_end : float
        Конечное время интегрирования.
    h : float
        Шаг интегрирования метода Эйлера.
    pairs : list[tuple[str, str]] or None, default: [('V', 'C'), ('V', 'F'), ('C', 'F'), ('V', 'm')]
        Пары переменных для проекций. Если None, используются стандартные пары.
    grid_density : int, default: 15
        Плотность сетки для векторного поля.
    stream_options : dict or None, default: {'color': 'gray', 'density': 1.0}
        Параметры `streamplot` для пар: {(var1, var2): {params}}.
    euler_options : dict or None, default: {'color': 'blue', 'lw': 1.5}
        Параметры траекторий для пар: {(var1, var2): {params}}.
    var_ranges : dict or None, default: {'V': (-10, 10), 'C': (-10, 10), 'F': (-10, 10), 'm': (-10, 10)}
        Диапазоны значений для переменных: {var: (min, max)}.
    axis_limits : dict or None, default: {}
        Границы осей для пар: {(var1, var2): (xlim, ylim)}.

    Returns
    -------
    tuple[list[float], list[float], list[float], list[float], list[float]]
        Кортеж из временных точек и значений переменных:
        - t_vals: временные точки
        - V_vals, C_vals, F_vals, m_vals: значения переменных

    Examples
    --------
    >>> # Построение фазового портрета для системы с задержкой
    >>> params = {
    ...     'beta': 1.0, 'gamma': 0.8, 'alpha': 100,
    ...     'mu_C': 0.9, 'C_star': 1, 'rho': 0.01,
    ...     'mu_f': 0.2, 'eta': 0.01, 'sigma': 0.12,
    ...     'mu_m': 1.0, 'tau': 0.5, 't0': 0.0
    ... }
    >>> initial_conditions = [0.5, 0.5, 0.2, 0.0]
    >>> t_vals, V_vals, C_vals, F_vals, m_vals = plot_phase_portrait_4d(
    ...     funcs=[], 
    ...     initial_conditions=initial_conditions, 
    ...     params=params, 
    ...     t_end=25.0, 
    ...     h=0.001,
    ...     pairs=[('V', 'C'), ('V', 'F')],
    ...     grid_density=50
    ... )

    Notes
    -----
    1. Уравнения системы жестко заданы в `euler_delay_system`, что ограничивает гибкость .
    2. Векторные поля рассчитываются при фиксированных начальных значениях других переменных, что упрощает визуализацию .
    3. Метод Эйлера имеет первый порядок точности, что может приводить к накоплению ошибки при больших временах интегрирования .
    4. Для улучшения устойчивости рекомендуется использовать адаптивные шаги или неявные методы .

    References
    ----------
    .. [4] "How to plot the phase portrait for 4×4 ODE system?" - (https://example.com/phase-4d)
    .. [1] "Phase portrait - Wikipedia" - (https://en.wikipedia.org/wiki/Phase_portrait)
    .. [2] "MATHEMATICA TUTORIAL, Part 1.2: Phase portrait" - (https://mathematica.stackexchange.com/questions/phase-portrait)
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Настройки по умолчанию
    default_stream_options = {'color': 'gray', 'density': 1.0}
    default_euler_options = {'color': 'blue', 'lw': 1.5}
    default_var_ranges = {var: (-10, 10) for var in ['V', 'C', 'F', 'm']}

    stream_options = stream_options or {}
    euler_options = euler_options or {}
    var_ranges = var_ranges or default_var_ranges
    axis_limits = axis_limits or {}

    # Используемые переменные
    variables = ['V', 'C', 'F', 'm']

    # Если пары не указаны, построить основные
    if pairs is None:
        pairs = [('V', 'C'), ('V', 'F'), ('C', 'F'), ('V', 'm')]

    # Решение системы
    t_vals, V_vals, C_vals, F_vals, m_vals = euler_delay_system(
        funcs, initial_conditions, params, t_end, h
    )
    var_values = {'V': V_vals, 'C': C_vals, 'F': F_vals, 'm': m_vals}

    # Подготовка графиков
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    # Построение для каждой пары
    for ax, (var1, var2) in zip(axes, pairs):
        # Получение параметров для текущей пары
        so = stream_options.get((var1, var2), default_stream_options)
        eo = euler_options.get((var1, var2), default_euler_options)

        # Использовать axis_limits, если они заданы
        if (var1, var2) in axis_limits:
            xlim, ylim = axis_limits[(var1, var2)]
            xr, yr = xlim, ylim
        else:
            xr = var_ranges.get(var1, default_var_ranges[var1])
            yr = var_ranges.get(var2, default_var_ranges[var2])

        # Создание сетки
        x_vals = np.linspace(*xr, grid_density)
        y_vals = np.linspace(*yr, grid_density)
        X, Y = np.meshgrid(x_vals, y_vals)

        # Вычисление производных
        U, V = np.zeros_like(X), np.zeros_like(Y)
        fixed_vars = {var: var_values[var][0] for var in variables if var not in (var1, var2)}

        for i in range(grid_density):
            for j in range(grid_density):
                current_vars = {var1: X[i, j], var2: Y[i, j], **fixed_vars}
                ordered_vars = [current_vars[var] for var in variables]
                derivatives = [func(0, ordered_vars) for func in funcs]
                idx1, idx2 = variables.index(var1), variables.index(var2)
                U[i, j] = derivatives[idx1]
                V[i, j] = derivatives[idx2]

        # Построение векторного поля и траектории
        ax.streamplot(X, Y, U, V, **so)
        ax.plot(var_values[var1], var_values[var2], **eo)

        # Настройка графика
        ax.set_title(f'Фазовый портрет ({var1}-{var2})')
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        ax.grid(True)

        # Установка границ осей
        if (var1, var2) in axis_limits:
            ax.set_xlim(axis_limits[(var1, var2)][0])
            ax.set_ylim(axis_limits[(var1, var2)][1])
        else:
            ax.set_xlim(min(var_values[var1]), max(var_values[var1]))
            ax.set_ylim(min(var_values[var2]), max(var_values[var2]))

    # Удаление лишних графиков
    for k in range(len(pairs), 4):
        fig.delaxes(axes[k])

    plt.tight_layout()
    plt.show()
    
    return t_vals, V_vals, C_vals, F_vals, m_vals
####################################################################################

####################################################################################
DF = [
    euler_method,
    plot_euler_solutions,
    euler_system,
    plot_phase_portrait_with_streamplot,
    plot_phase_portrait_3d,
    euler_delay_system,
    plot_phase_portrait_4d
]