from ...forall import *
#######################################################################################################################
# Нормальные случайные векторы ДОПОЛНИТЕЛЬНЫЙ ПАКЕТ ФУНКЦИЙ
#######################################################################################################################
def ANRV_1(a,b,n):
    """Случайный вектор(X,Y) равномерно распределен в треугольнике x⩾0, y⩾0, `a`*x+y⩽`b`.
    Найдите математическое ожидание E(X^`n` * Y).

    Args:
        a (numerical): `a`*x+y⩽b
        b (numerical): a*x+y⩽`b`

    Returns:
        EX10Y: математическое ожидание E(X^`n` * Y)
    """
    import sympy
    
    x,y = sympy.symbols('x y',real=True)

    f = 1/sympy.integrate(1,(y,0,b-a*x),(x,0,1))

    EX10Y = sympy.integrate(f* x**n * y,(y,0,b-a*x),(x,0,1))
    print(EX10Y)    

    return EX10Y
#######################################################################################################################
def ANRV_2(a,x_1,x_2,y_1,y_2,p):
    """Случайный вектор имеет плотность распределения f(x,y) =`a`*x + C*y , `x_1` < x < `x_2`, `y_1` < y < `y_2`,
    найдите константу C и вероятность P(X + Y > `p`)

    Args:
        a (numerical): Коэффициент при x
        x_1 (numerical): Левая граница значений x
        x_2 (numerical): Правая граница значений x
        y_1 (numerical): Левая граница значений y
        y_2 (numerical): Правая граница значений y
        p (numerical): P(X + Y > `p`)

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до 4 знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    
    import sympy
    x, y, C = sympy.symbols('x y C')
    
    f = a * x + C*y
    
    i = sympy.integrate(f, (y, y_1, y_2), (x,x_1, x_2))
    
    c0 = sympy.solve(i - 1)[0]
    f = f.subs(C, c0)

    answer = (c0,sympy.integrate(f, (y, -x+p, y_2), (x,x_1, x_2)))
    
    print('Константа C = ' + rrstr(answer[0],4))
    print(f'P(X+Y>{p}) = ' + rrstr(answer[0],4))
    
    return answer
#######################################################################################################################
def ANRV_3(C,a,b,p):
    """Случайный вектор (X,Y) имеет плотность распределения f(x,y)= `C`*e^(`a`*x+`b`*y),
    если 0 ⩽ x < +∞, 0 ⩽ y < +∞, 0, в остальных точках. Найдите вероятность P(X < `p`).    

    Args:
        C (numerical): Коэффициент при экспоненте
        a (numerical): Коэффициент при x
        b (numerical): Коэффициент при y
        p (numerical): P(X < `p`)

    Returns:
        answer(numerical): Вероятность P(X < `p`)
    """
    import sympy
    
    assert a*b==C, 'C должно быть равно a*b'
    
    x, y = sympy.symbols('x y')
    f = C*sympy.exp(a*x+b*y)
    
    answer = sympy.integrate(f,(y,0,'oo'),(x,0,p))
    
    return answer
#######################################################################################################################
def ANRV_4(c_x2 = 0,c_x = 0,c_xy = 0,c_y = 0,c_y2 = 0):
    """Случайный вектор (X,Y) имеет плотность распределения<br>
    f_X,Y(x,y) = ( [невлияющий коэф.] * e^-1/2*(c_x2 * x^2 + c_x * x + c_xy * xy + c_y * y + c_y2 * y^2 + [невлияющая константа]) / π
    
    Найдите:
    - математическое ожидание E(X)
    - математическое ожидание E(Y)
    - дисперсию  Var(X)
    - дисперсию  Var(Y)
    - ковариацию  Cov(X,Y)
    - коэффициент корреляции  ρ(X,Y)
    - математическое ожидание E(X|Y)
    - математическое ожидание E(Y|X)
    - дисперсию  Var(X|Y)
    - дисперсию  Var(Y|X)
    
    Args:
        c_x2 (numerical, optional): Коэффициент при x^2. По умолчанию 0.
        c_x (numerical, optional): Коэффициент при x. По умолчанию 0.
        c_xy (numerical, optional): Коэффициент при xy. По умолчанию 0.
        c_y (numerical, optional): Коэффициент при y. По умолчанию 0.
        c_y2 (numerical, optional): Коэффициент при y^2. По умолчанию 0.
        
    ## Prints
        `answer` каждое значение по очереди. Без округления

    Returns:
        answer (tuple): (`sol[EX]`, `sol[EY]`, `VarX`, `VarY`, `CovXY`, `roXY`,`EX_Y`,`EY_X`,`VarX_Y`,`VarY_X`)
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
    
    x,y = sympy.symbols('x y',real=True)

    EX_Y=sol[EX]+roXY*sigmaX/sigmaY*(y-sol[EY])
    EY_X=sol[EY]+roXY*sigmaY/sigmaX*(x-sol[EX])

    VarX_Y=sigmaX**2*(1-roXY**2)
    VarY_X=sigmaY**2*(1-roXY**2)
    print(f'EX = {sol[EX]}\nEY = {sol[EY]}\nVarX = {VarX}\nVarY = {VarY}\nCovXY = {CovXY}\nroXY = {roXY}\nEX_Y = {EX_Y}\nEY_X = {EY_X}\nVarX_Y = {VarX_Y}\nVarY_X = {VarY_X}')
    
    answer = (sol[EX],sol[EY],VarX,VarY,CovXY,roXY,EX_Y,EY_X,VarX_Y,VarY_X)

    return answer
#######################################################################################################################
ANRV=[ANRV_1,ANRV_2,ANRV_3,ANRV_4]