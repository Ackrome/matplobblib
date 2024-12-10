#######################################################################################################################
# Выборки из конечной совокупности
#######################################################################################################################
def SFFP_1(Omega, n):
    """В группе Ω учатся `N` студентов, Ω={1,2,...,`N`}.
    Пусть X(i) – 100-балльная оценка студента i∈Ω.
    Из группы Ω случайным образом `n` раз выбирается студент ω∈Ω.
    Повторный выбор допускается. Пусть ωj – студент,
    полученный после выбора j=1,...,`n`, X(ωj)– его оценка.
    Среднюю оценку на случайной выборке обозначим X¯=1/`n` * ∑X(ωj).
    Оценки в группе даны: `Omega`. Требуется найти:
    - дисперсию Var(X¯)
    - центральный момент μ3(X¯)

    Args:
        Omega (str): Список оценок для студентов
        n (int): Размер выборки

    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    Returns:
        `answer` (tuple): Соответствующие значения
    """
    import scipy.stats as st
    import numpy as np

    Omega = np.array(Omega.split(', ')).astype(int)

    Var = Omega.var(ddof=0)/n
    mu3 = st.moment(Omega, 3)/n**2
    answer = [Var, mu3]
    
    print(f'Дисперсия Var(X¯) = {rrstr(answer[0],3)}')
    print(f'Центральный момент μ3(X¯) = {rrstr(answer[1],3)}')
    
    return answer
#######################################################################################################################
def SFFP_2(Omega, n):
    """В группе Ω учатся `N` студентов, Ω={1,2,...,`N`}.
    Пусть X(i) – 100-балльная оценка студента i∈Ω.
    Из группы Ω случайным образом `n` раз выбирается студент ω∈Ω.
    Повторный выбор НЕ допускается. Пусть ωj – студент,
    полученный после выбора j=1,...,`n`, X(ωj)– его оценка.
    Среднюю оценку на случайной выборке обозначим X¯=1/`n` * ∑X(ωj).
    Оценки в группе даны: `Omega`. Требуется найти:
    - математическое ожидание E(X¯)
    - дисперсию Var(X¯)

    Args:
        Omega (str): Список оценок для студентов
        n (int): Размер выборки

    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    Returns:
        `answer` (tuple): Соответствующие значения
    """
    import scipy.stats as st
    import numpy as np

    Omega = np.array(Omega.split(', ')).astype(int)

    mu = Omega.mean()
    Var = Omega.var()/n *  (Omega.size - n)/(Omega.size -1)

    answer = [mu,Var]
    
    print(f'математическое ожидание E(X¯) = {rrstr(answer[0],3)}')
    print(f'Дисперсия Var(X¯) = {rrstr(answer[1],3)}')
    
    
    return answer
#######################################################################################################################
def SFFP_3(marks, works, n_prep):
    """Распределение баллов на экзамене до перепроверки задано таблицей<br>
    `marks`<br>
    `works`<br>
    Работы будут перепроверять `n_prep` преподавателей, которые разделили
    все работы между собой поровну случайным образом.
    Пусть X¯ – средний балл (до перепроверки) работ,
    попавших к одному из преподавателей.
    Требуется найти:
    - математическое ожидание E(X¯);
    - стандартное отклонение σ(X¯).

    Args:
        marks (list): список оценок
        works (list): спиосок количеств работ
        n_prep (int): количество преподавателей

    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    Returns:
        `answer` (tuple): Соответствующие значения
    """
    import numpy as np

    X = np.repeat(marks, works)
    mu = X.mean()
    s = X.std() * np.sqrt((X.shape[0] - X.shape[0]/n_prep)/(X.shape[0]/n_prep * (X.shape[0]-1)) )
    
    print('Математическое ожидание = ' + rrstr(mu,2))
    print('Стандартное отклонение = ' + rrstr(s,3))
    
    answer = [mu, s]
    
    return answer
#######################################################################################################################
def SFFP_4(text):
    """Две игральные кости, красная и синяя, подбрасываются до тех пор,
    пока не выпадет `n` различных (с учетом цвета) комбинаций очков.
    Пусть Ri – число очков на красной кости, а Bi – число очков на
    синей кости в комбинации с номером i.
    Случайные величины Xi задаются соотношениями: Xi=... ,i=1,...,`n`.
    Среднее арифметическое этих величин обозначим X¯=1/`n`∑Xi.
    Требуется найти: 
    - математическое ожидание E(X¯)
    - стандартное отклонение σ(X¯)
    
    Args:
        text (long-str): текст условия задачи
    
    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    Returns:
        `answer` (tuple): Соответствующие значения
    """
    import re
    import numpy as np
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string")
    text = text.replace("−", "-")
    try:
        coefficients = re.findall(r'([-+]?\d+)\s*R[iI]|([-+]?\d+)\s*B[iI]', text)
        coeff_Ri = int(coefficients[0][0]) if coefficients[0][0] else 0
        coeff_Bi = int(coefficients[1][1]) if coefficients[1][1] else 0
    except IndexError:
        raise ValueError("Failed to extract coefficients from text")

    try:
        match = re.findall(r'\b(\d+)\b\s+различных', text)
        n_combinations = int(match[0])
    except IndexError:
        raise ValueError("Failed to extract number of combinations from text")

    ribi = np.array([coeff_Ri, coeff_Bi])
    r_values = np.arange(1,7)
    e_r = r_values.sum()/r_values.size
    var_r = (r_values**2).sum()/r_values.size -e_r**2
    N = 6**2

    try:
        E_X = np.multiply(ribi, e_r).sum()
        s = np.sqrt(np.multiply(ribi**2, var_r).sum() / n_combinations * (N - n_combinations) / (N - 1))
    except (RuntimeError, ValueError) as e:
        raise RuntimeError("Numerical error: {}".format(e))

    answer = [E_X, s]

    print(rrstr(answer[0],1))
    print(rrstr(answer[1],3))
    
    return answer
#######################################################################################################################
def SFFP_5(n_coins, n_combinations):
    """Имеется `n_coins` пронумерованных монет.
    Монеты подбрасываются до тех пор, пока не выпадет `n_combinations` различных
    (с учетом номера монеты) комбинаций орел-решка.
    Пусть Xi – число орлов в комбинации с номером i;
    а X¯ = 1/`n_combinations` * ∑Xi – среднее число орлов в полученных таким образом комбинациях.
    Требуется найти:
    - математическое ожидание E(¯)
    - дисперсию Var(X¯)
    
    Args:
        n_coins (int): количество пронумерованных монет
        n_combinaations (int): количество различных комбинаций
        
    
    ## Prints
        `answer` каждое значение последовательно.<br>C запятой вместо точки и сокращенное до соответствующего количества десятичных знаков.

    Returns:
        `answer` (tuple): Соответствующие значения
    """
    import numpy as np
    import scipy.stats
    
    X = scipy.stats.binom(n_coins,1/2)
    N = 2**n_coins
    answer = [n_coins/2, X.var() /n_combinations * (N-n_combinations)/(N-1) ]
    
    print('Математическое ожидание = ' + rrstr(answer[0],1))
    print('Дисперсия = ' + rrstr(answer[1],3))
    
    return answer
#######################################################################################################################
def SFFP_6(X,Y,n_XY,n):
    """Эмпирическое распределение признаков X и Y
    на генеральной совокупности Ω={1,2,...,100} задано таблицей частот.
    Из Ω случайным образом без возвращения извлекаются 6 элементов. Пусть X¯
    и Y¯ – средние значения признаков на выбранных элементах.
    Требуется найти:
    - математическое ожидание E(X¯)
    - дисперсию Var(Y¯)
    - коэффициент корреляции ρ(X¯,Y¯)

    Args:
        X (list): Все значения, которые принимает X
        Y (list): Все значения, которые принимает Y
        n_XY (list): Значения таблицы частот двумерным списком
        n (int): количество элементов, извлекаемых без возвращения
        
    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    from IPython.display import Math
    import numpy as np
    
    X = np.array(X)
    Y = np.array(Y)
    n_XY = np.array(n_XY)
    N = n_XY.sum()

    N = n_XY.sum()                  # Всего элементов в генеральной совокупности
    p_X = n_XY.sum(axis=1) / N  # частоты для X
    p_Y = n_XY.sum(axis=0) / N  # частоты для Y

    E_X = (X * p_X).sum()
    E_Y = (Y * p_Y).sum()

    # Найдем дисперсии Var(X) и Var(Y)
    Var_X = ((X) ** 2 * p_X).sum()  - E_X**2
    Var_Y = ((Y) ** 2 * p_Y).sum()  - E_Y**2
    Var_Y=np.dot(np.power(Y, 2), p_Y) - E_Y**2

    # Найдем ковариацию Cov(X, Y)
    cov_XY = 0
    for i in range(len(X)):
        for j in range(len(Y)):
            p_xy = n_XY[i, j] / N
            cov_XY += p_xy * (X[i] - E_X) * (Y[j] - E_Y)

    # Дисперсии выборочных средних
      # размер выборки
    Var_X_bar = Var_X /n * (N-n)/(N-1)
    Var_Y_bar = Var_Y /n * (N-n)/(N-1)

    # Ковариация выборочных средних
    Cov_XY_bar = cov_XY /n * (N-n)/(N-1)

    # Коэффициент корреляции 
    rho_XY = cov_XY / np.sqrt(Var_X * Var_Y)
    
    answer = [E_X, Var_Y_bar,rho_XY ]

    display(Math(('Математическое ожидание \mathbb{E}(\overline{X}) = ' + f'{rrstr(answer[0],3)}').replace(' ','~')))
    display(Math(('Дисперсия \mathbb{Var}(\overline{Y}) = ' + f'{rrstr(answer[1],3)}').replace(' ','~')))
    display(Math(('Коэффициент корреляции r(\overline{X},\overline{Y}) = ' + f'{rrstr(answer[2],3)}').replace(' ','~')))

    return answer
#######################################################################################################################
def SFFP_7(X,Y,n_XY,n):
    """Эмпирическое распределение признаков X и Y
    на генеральной совокупности Ω={1,2,...,100} задано таблицей частот.
    Из Ω случайным образом без возвращения извлекаются 6 элементов. Пусть X¯
    и Y¯ – средние значения признаков на выбранных элементах.
    Требуется найти:
    - математическое ожидание E(Y¯)
    - стандартное отклонение σ(X¯)
    - ковариацию Cov(X¯,Y¯)

    Args:
        X (list): Все значения, которые принимает X
        Y (list): Все значения, которые принимает Y
        n_XY (list): Значения таблицы частот двумерным списком
        n (int): количество элементов, извлекаемых без возвращения

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    from IPython.display import Math
    import numpy as np
    X = np.array(X)
    Y = np.array(Y)
    n_XY = np.array(n_XY)
    N = n_XY.sum()

    N = n_XY.sum()                  # Всего элементов в генеральной совокупности
    p_X = n_XY.sum(axis=1) / N  # частоты для X
    p_Y = n_XY.sum(axis=0) / N  # частоты для Y

    E_X = (X * p_X).sum()
    E_Y = (Y * p_Y).sum()

    # Найдем дисперсии Var(X) и Var(Y)
    Var_X = ((X - E_X) ** 2 * p_X).sum()
    Var_Y = ((Y - E_Y) ** 2 * p_Y).sum()

    # Найдем ковариацию Cov(X, Y)
    cov_XY = 0
    for i in range(len(X)):
        for j in range(len(Y)):
            p_xy = n_XY[i, j] / N
            cov_XY += p_xy * (X[i] - E_X) * (Y[j] - E_Y)

    # Дисперсии выборочных средних
    Var_X_bar = Var_X /n * (N-n)/(N-1)
    Var_Y_bar = Var_Y /n * (N-n)/(N-1)

    # Ковариация выборочных средних
    Cov_XY_bar = cov_XY /n * (N-n)/(N-1)

    # Коэффициент корреляции выборочных средних
    rho_XY_bar = Cov_XY_bar / (np.sqrt(Var_X_bar) * np.sqrt(Var_Y_bar))

    answer = [E_Y, Var_X_bar**0.5, Cov_XY_bar]
    
    display(Math(('Математическое ожидание \mathbb{E}(\overline{Y}) = ' + f'{rrstr(answer[0],3)}').replace(' ','~')))
    display(Math(('Стандартное отклонение \sigma(\overline{X}) = ' + f'{rrstr(answer[1],3)}').replace(' ','~')))
    display(Math(('Ковариация \mathbb{Cov}(\overline{X},\overline{Y}) = ' + f'{rrstr(answer[2],3)}').replace(' ','~')))

    return answer
#######################################################################################################################
SFFP = [SFFP_1,SFFP_2,SFFP_3,SFFP_4,SFFP_5,SFFP_6,SFFP_7]