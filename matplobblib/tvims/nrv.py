from .rrstr import *
#######################################################################################################################
# Нормальные случайные векторы
#######################################################################################################################
def NRV_1(muX,muY,sigmaX2,sigmaY2,rho,Px,Py):
    """Для нормального случайного вектора<br>
    (X,Y) ∼ N(muX, muY, sigmaX2, sigmaY2, rho)<br>
    Найдите вероятность P((X - Px)(Y - Py) < 0).

    Args:
        muX (numerical): Математическое ожидание X
        muY (numerical): Математическое ожидание Y
        sigmaX2 (numerical): Дисперсия X
        sigmaY2 (numerical): Дисперсия Y
        rho (numerical): Коэффициент корреляции между X и Y
        Px (numerical): Число для вычитания из X
        Py (numerical): Число для вычитания из Y

    ## Prints
        P((X - Px)(Y - Py) < 0) = `answer` с запятой вместо точки и сокращением до 4 знаков после запятой
    
    Returns:
        answer (numerical): Вероятность P((X - Px)(Y - Py) < 0)
    """
    ''''''
    
    import math
    import numpy as np
    import scipy.stats
    
    N = {'muX': muX, 'muY': muY, 'sigmaX2': sigmaX2, 'sigmaY2': sigmaY2, 'rho': rho}
    mu = np.array([N['muX'], N['muY']])
    Cov = np.array([[N['sigmaX2'], N['rho']*math.sqrt(N['sigmaX2'])*math.sqrt(N['sigmaY2'])],
                    [N['rho']*math.sqrt(N['sigmaX2'])*math.sqrt(N['sigmaY2']), N['sigmaY2']]])
    W = scipy.stats.multivariate_normal(mu, Cov)
    X = scipy.stats.norm(N['muX'], math.sqrt(N['sigmaX2']))
    Y = scipy.stats.norm(N['muY'], math.sqrt(N['sigmaY2']))
    Pa=X.cdf(Px)-W.cdf([Px,Py])
    Pb=Y.cdf(Py)-W.cdf([Px,Py])
    
    answer=Pa+Pb
    
    print(f'P((X-{Px})(Y-{Py})<0) = {rrstr(answer,4)}')
    
    return answer
#######################################################################################################################
def NRV_2(muX,muY,sigmaX2,sigmaY2,rho,xminus1,xminus2,yminus):
    """Для нормального случайного вектора <br>
    (X,Y) ∼ N(muX,muY,sigmaX2,sigmaY2,rho)<br>
    Найдите вероятность P((X - xminus1)(X - xminus2)(Y - yminus) < 0).

    Args:
        muX (numerical): Математическое ожидание X
        muY (numerical): Математическое ожидание Y
        sigmaX2 (numerical): Дисперсия X
        sigmaY2 (numerical): Дисперсия Y
        rho (numerical): Коэффициент корреляции между X и Y
        xminus1 (numerical): Первое число для вычитания из X
        xminus2 (numerical): Второе число для вычитания из X
        yminus (numerical): Число для вычитания из Y

    ## Prints
        P((X - xminus1)(X - xminus2)(Y - yminus) < 0) = `answer` с запятой вместо точки и сокращением до 4 знаков после запятой

    Returns:
        answer (numerical): Вероятность P((X - xminus1)(X - xminus2)(Y - yminus) < 0)
    """ 
    import numpy as np
    import scipy.stats
    
    np.abs
    
    sigmaX = sigmaX2**0.5
    sigmaY = sigmaY2**0.5
    
    mu = np.array([muX,muY])
    Cov = np.array([[sigmaX**2, rho*sigmaX*sigmaY], [rho*sigmaX*sigmaY, sigmaY**2]])
    
    X = scipy.stats.norm(muX, sigmaX)
    Y = scipy.stats.norm(muY, sigmaY)
    W = scipy.stats.multivariate_normal(mu, Cov)
    
    Pa = W.cdf([xminus1, yminus])
    Pb = X.cdf(xminus2) - X.cdf(xminus1) - (W.cdf([xminus2, yminus]) - W.cdf([xminus1, yminus]))
    Pc = Y.cdf(yminus) - W.cdf([xminus2, yminus])
    
    answer = Pa+Pb+Pc
    
    print(f'P((X - {xminus1})(X - {xminus2})(Y - {yminus}) < 0) = {rrstr(answer,4)}')
    
    return answer
#######################################################################################################################
def NRV_3(c_x2 = 0,c_x = 0,c_xy = 0,c_y = 0,c_y2 = 0):
    """Случайный вектор (X,Y) имеет плотность распределения<br>
    f_X,Y(x,y) = ( [невлияющий коэф.] * e^-1/2*(c_x2 * x^2 + c_x * x + c_xy * xy + c_y * y + c_y2 * y^2 + [невлияющая константа]) / π
    
    Найдите:
    - математическое ожидание E(X)
    - математическое ожидание E(Y)
    - дисперсию  Var(X)
    - дисперсию  Var(Y)
    - ковариацию  Cov(X,Y)
    - коэффициент корреляции  ρ(X,Y)

    Args:
        c_x2 (numerical, optional): Коэффициент при x^2. По умолчанию 0.
        c_x (numerical, optional): Коэффициент при x. По умолчанию 0.
        c_xy (numerical, optional): Коэффициент при xy. По умолчанию 0.
        c_y (numerical, optional): Коэффициент при y. По умолчанию 0.
        c_y2 (numerical, optional): Коэффициент при y^2. По умолчанию 0.

    ## Prints
        EX = `sol[EX]`, EY = `sol[EY]`, VarX = `VarX`, VarY = `VarY`, CovXY = `CovXY`, roXY = `roXY`

    Returns:
        answer (tuple): (`sol[EX]`, `sol[EY]`, `VarX`, `VarY`, `CovXY`, `roXY`)
    """
    import sympy
    #после выноса -1/2!!!!!!
    coefs = {
        'x^2': c_x2,
        'x': c_x,
        'xy': c_xy,
        'y': c_y,
        'y^2': c_y2,
    }
    C = sympy.Matrix([[coefs['x^2'], int(coefs['xy']/2)], [int(coefs['xy']/2), coefs['y^2']]])
    C1 = C**(-1)
    VarX = C1[0, 0]
    sigmaX = sympy.sqrt(VarX)
    VarY = C1[1, 1]
    sigmaY = sympy.sqrt(VarY)
    CovXY = C1[0, 1]
    roXY = CovXY/(sigmaX*sigmaY)
    EX, EY = sympy.symbols('EX, EY')
    equations = (
        sympy.Eq(int(coefs['x^2'])*EX + int(coefs['xy']/2)*EY, int(coefs['x']*(-1/2))),
        sympy.Eq(int(coefs['xy']/2)*EX + int(coefs['y^2'])*EY, int(coefs['y']*(-1/2)))
    )
    sol = sympy.solve(equations, (EX, EY))
    
    print(f'EX = {sol[EX]}, EY = {sol[EY]}, VarX = {VarX}, VarY = {VarY}, CovXY = {CovXY}, roXY = {roXY}')
    
    answer = (sol[EX],sol[EY],VarX,VarY,CovXY,roXY)
    
    return answer
#######################################################################################################################
NRV=[NRV_1,NRV_2,NRV_3] # Список функций в файле