def imports():
    return '''
    from scipy.stats import *
    from scipy.integrate import quad
    import math
    import numpy a np
    import sympy
    import itertools
    sympy.init_printing(use_unicode=True,use_latex=True)
    '''
    
def enable_ppc():
    return '''    import pyperclip

    #Делаем функцию которая принимает переменную text
    def write(name):
        pyperclip.copy(name) #Копирует в буфер обмена информацию
        pyperclip.paste()'''
        
#ContinuousRandomVariables
def CRV_1():
    task = 'Абсолютно непрерывная случайная величина  X  может принимать значения только в отрезке [a, b]. На этом отрезке плотность распределения случайной величины  X  имеет вид: f(x)=C(1+a^0.1+2b^0.2+3c^0.3)^1.1, где С - положительная константа. Найти:\n- константу C математическое ожидание E(X)\n- стандартное отклонение σX\n- квантиль уровня k распределения X'
    answer = '\n#условие\n# [a,b]\na,b = 4,9\n# F = f(x) без C\nF = lambda x: (1 + 7*x**(0.5) + 8*x**(0.7) + 4*x**(0.9))**(1.3)\nC = 1 / integrate.quad(F, a, b)[0]\ndef f(x):\n    return C * F(x)\nclass dist_f_C(rv_continuous):\n  #функция вероятности\n  def _pdf(self,x):\n    return f(x) if (a<= x <=b) else 0\n  #функция значений\n  def _expect(self,x):\n    return x\n#зададим распределение\nf_C = dist_f_C(a = a, b = b)\n#1\nprint(f"C = {C}")\n#2\nprint(f"E = {f_C.mean()}")\n#3\nprint(f"sigma = {f_C.std()}")\n#4\nprint(f"q = {f_C.ppf(0.9)}")\n'

    return [task,answer]
def CRV_2():
    task = 'Случайная величина X равномерно распределена на отрезке [a,b]. Случайная величина Y выражается через X следующим образом: Y = (1+a^0.1+2b^0.2+3c^0.3)^1.1. Найдите:\n- математическое ожидание  E(Y)\n- стандартное отклонение σY\n- асимметрию As(Y)\n- квантиль уровня 0,8 распределения Y'
    answer = '\nF = lambda x: (1 + 6*x**0.5 + 4*x**0.7 + 5 * x**0.9)**1.3\nab = [4, 8]\np = 1/(ab[1]-ab[0])\nEY = p * integrate.quad(F, 4, 8)[0]\nprint(f"EY = {EY}")\nf = lambda x: (F(x))**2\nVarY = p * integrate.quad(f, 4, 8)[0] - EY**2\nQy = math.sqrt(VarY)\nprint(f"Qy = {Qy}")\nf = lambda x: p * (F(x) - EY)**3\nAsY = integrate.quad(f, 4, 8)[0]/Qy**3\nprint(f"AsY = {AsY}")\n#q_l = quantile_level\nq_l = 0.8\n# работает при равномерном случайном распределении!\nq = F(ab[0] + (ab[1] - ab[0])*q_l)\nprint(f"q = {q}")\n'
    return [task,answer]

#NormalRandomVectors
def NRV_1():
    task = 'Для нормального случайного вектора (X,Y)∼N(−8;16;49;1;0,8) найдите вероятность P((X−3)(Y−7)<0).'
    answer = "\nN = {'muX': -8, 'muY': 16, 'sigmaX2': 49, 'sigmaY2': 1, 'rho': 0.8}\nmu = np.array([N['muX'], N['muY']])\nCov = np.array([[N['sigmaX2'], N['rho']*math.sqrt(N['sigmaX2'])*math.sqrt(N['sigmaY2'])],\n                [N['rho']*math.sqrt(N['sigmaX2'])*math.sqrt(N['sigmaY2']), N['sigmaY2']]])\nW = multivariate_normal(mu, Cov)\nX = norm(N['muX'], math.sqrt(N['sigmaX2']))\nY = norm(N['muY'], math.sqrt(N['sigmaY2']))\nPx = 3\nPy = 7\nPa=X.cdf(Px)-W.cdf([Px,Py])\nPb=Y.cdf(Py)-W.cdf([Px,Py])\nPa+Pb\n"
    return [task,answer]
def NRV_2():
    task = 'Для нормального случайного вектора (X,Y)∼N(−4;4;64;81;−0,31) найдите вероятность P((X−8)(X−10)(Y−1)<0).'
    answer = "\n#Смотрим на распределение, которое задано\nmuX = -4\nmuY = 4\nsigmaX = 64**0.5\nsigmaY = 81**0.5\nrho = -0.31\n#Смотрим на вероятность, которую хотят от нас\nxminus1 = 8\nxminus2 = 10\nyminus = 1\nmu = np.array([muX,muY])\nCov = np.array([[sigmaX**2, rho*sigmaX*sigmaY], [rho*sigmaX*sigmaY, sigmaY**2]])\nX = norm(muX, sigmaX)\nY = norm(muY, sigmaY)\nW = multivariate_normal(mu, Cov)\nPa = W.cdf([xminus1, yminus])\nPb = X.cdf(xminus2) - X.cdf(xminus1) - (W.cdf([xminus2, yminus]) - W.cdf([xminus1, yminus]))\nPc = Y.cdf(yminus) - W.cdf([xminus2, yminus])\nPa+Pb+Pc\n"
    return [task,answer]
def NRV_3():
    task = 'Случайный вектор (X,Y) имеет плотность распределения fX,Y(x,y)=(18e^(−30x2−48xy+8x−30y2−5y−8524))\π\nНайдите:\n- математическое ожидание E(X)\n-математическое ожидание E(Y)\n-дисперсию  Var(X)\n-дисперсию  Var(Y)\n-ковариацию  Cov(X,Y)\n-коэффициент корреляции  ρ(X,Y)'
    answer = '''
            #после выноса -1/2!!!!!!
        coefs = {
            'x^2': 60,
            'x': -16,
            'xy': 96,
            'y': 10,
            'y^2': 60,
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
        '''
    return [task,answer]

#FullProbabilityAndBayesianFormulas
def FPB_1():
    task = 'Имеется 37 монет, из которых 6 бракованные: вследствие заводского брака на этих монетах с обеих сторон отчеканен герб. Наугад выбранную монету, не разглядывая, бросают несколько раз. 1) Какова вероятность, что при 4 бросках она ляжет гербом вверх? 2) При 4 бросках монета легла гербом вверх. Какова вероятность того, что была выбрана монета с двумя гербами?'
    answer ='''
    coins = [('O', 'P')]*31 + [('O', 'O')]*6
    count_1 = 0
    count_2 = 0
    N = 0
    for coin in coins:
        for throws in list(itertools.product(coin, repeat=4)):
            throw = ''.join(throws)
            N += 1
            if 'OOOO' in throw:
                count_1 += 1
                if coin == ('O', 'O'):
                    count_2 += 1
    print(count_1/N,count_2/count_1)
    '''
    return [task,answer]
def FPB_2():
    task='''
    В первой корзине имеется 8 шаров, при этом количество белых шаров равно либо 5, либо 8. 
    Оба варианта равновероятны. 
    Во второй корзине имеется 26 шаров, а количество белых шаров равно 7, 11 или 23. 
    Эти три варианта также равновероятны. 
    Из обеих корзин все шары перекладываются в третью корзину. 
    1) Какова вероятность $P(A)$, что случайно вынутый из третьей корзины шар окажется белым (событие $A$)?
    2) Найдите условную вероятность $P(H|A)$, того, что случайно вынутый из третьей корзины шар 
    первоначально находился в первой корзине (событие $H$), при условии, что он белый (событие $A$)?<br/>
    '''
    answer ='''
    first = 8
    first1 = 5
    first2 = 8
    Pfirst = 0.5

    second = 26
    second1 = 7
    second2 = 11
    second3 = 23
    Psecond = 1/3

    Pa = ((first1+first2)*Pfirst + (second1+second2+second3)*Psecond) / (first + second)
    rrstr(Pa,3) ,rrstr(((first1+first2)*Pfirst/first * (first/(first+second))) / Pa,3)
    '''
    return [task,answer]
def FPB_3():
    task='''
    Имеется две корзины с белыми и черными шарами. 
    В первой корзине всего 8 шаров, при этом количество белых шаров распределено по биномиальному закону с параметрами
    n = 6 и p = 0,3. 
    Во второй корзине имеется всего 9 шаров, при этом количество белых шаров распределено по биномиальному закону 
    с параметрами n = 3 и p = 0,8. Из обеих корзин все шары перекладываются в третью корзину. 
    1) Какова вероятность $P(A)$, что случайно вынутый из третьей корзины шар окажется белым (событие $A$)?
    2) Найдите условную вероятность $P(H|A)$, того, что случайно вынутый из третьей корзины шар 
    первоначально находился в первой корзине (событие $H$), при условии, что он белый (событие $A$)?
    '''
    answer ='''
    n1, p1 = 6, 0.3
    n2, p2 = 3, 0.8

    expected_white_balls1 = n1 * p1
    expected_white_balls2 = n2 * p2

    total_balls = 9 + 8

    P_A = (expected_white_balls1 + expected_white_balls2) / total_balls

    P_H = 9 / total_balls
    P_A_given_H = expected_white_balls1 / 9
    P_H_given_A = (P_A_given_H * P_H) / P_A

    print("P(A):", round(P_A, 3))
    print("P(H\A):", round(P_H_given_A, 3))
    '''
    return [task,answer]
def FPB_4():
    task='''
    Имеется две корзины с белыми и черными шарами. 
    В первой корзине количество белых – 16, количество черных – 17.
    Во второй корзине количество белых – 18, количество черных – 19.
    Из первой корзины случайно, без возвращения, излекаются 6 шаров, а из второй – 11 шаров.
    Отобранные из обеих корзин шары перекладываются в третью корзину. 
    1) Какова вероятность $P(A)$, что случайно вынутый из третьей корзины шар окажется белым (событие $A$)?
    2) Найдите условную вероятность $P(H|A)$, того, что случайно вынутый из третьей корзины шар 
    первоначально находился в первой корзине (событие $H$), при условии, что он белый (событие $A$)?
    '''
    answer ='''
    wt1, bl1 = 16, 17

    wt2, bl2 = 18, 19


    take1 = 6
    take2 = 11

    balls1 = wt1 + bl1
    balls2 = wt2 + bl2

    p_h1 = take1 / (take2 + take1)
    p_h2 = take2 / (take2 + take1)

    p_ah1 = wt1 / balls1
    p_ah2 = wt2 / balls2


    p_a = p_h1 * p_ah1 + p_h2 * p_ah2
    print(f"{p_a}".replace(".", ","))

    p_ha = p_h1 * p_ah1 / p_a
    print(f"{p_ha}".replace(".", ","))
    '''
    return [task,answer]

#SpecialDiscreteRandomVariables
def SDRV_1():
    task='''
    Банк выдал кредиты двум группам заемщиков: 210 заемщиков в первой группе и 270 – во второй. 
    Известно, что заемщики из первой группы возвращают кредит с вероятностью 0,94, а заемщики 
    из второй группы – с вероятностью 0,96. Пусть $X$ – суммарное количество возвращенных кредитов для обеих групп.
    Предполагая независимость заемщиков, найдите: 1) стандартное отклонение $X$; 2) асимметрию $X$. 
    '''
    answer='''
    na = 210
    nb = 270
    pa = 0.94
    pb = 0.96

    qa = 1-pa
    qb = 1-pb

    sigmaX = (na*pa*qa + nb*pb*qb)**0.5
    print('sigmaX:',rrstr(sigmaX,1))

    AsX = (na*pa*qa*(qa-pa) + nb*pb*qb*(qb-pb))/(sigmaX**3)
    print('AsX:',rrstr(AsX,3))
    '''
    return [task,answer]
def SDRV_2():
    task='''
    Независимые пуассоновские случайные величины X,Y,Z
    имеют следующие стандартные отклонения: σX=0,3
    ; σY=0,9
    ; σZ=1,8
    . Пусть S=X+Y+Z
    . Найдите:

    1) вероятность P(S=7)
    ;

    2) наиболее вероятное значение суммы S
    ;

    3) стандартное отклонение σS
    ;

    4) асимметрию As(S)
    ;

    5) эксцесс Ex(S)
    .
    '''
    answer ='''
    def P(k, A):
        return A**k / math.factorial(k) * math.e**(-A)

    #Дано
    sigmaX=0.3
    sigmaY=0.9
    sigmaZ=1.8

    AX = sigmaX**2
    AY = sigmaY**2
    AZ = sigmaZ**2

    S =  poisson(AX + AY + AZ)
    #1
    print(rrstr(S.pmf(7),3),'P(S=7) ')
    #2
    print(S.median(),'Наиболее вероятное S ')
    #3
    print(rrstr(S.std(),3),'стандартное отклонение σS ')
    #4
    AsS = (sigmaX**2 + sigmaY**2 + sigmaZ**2)/((S.var()**0.5)**3)
    print(rrstr(AsS,3),'асимметрия As(S)')
    #5
    numerator = (sigmaX**2 + sigmaY**2 + sigmaZ**2) + 3*(sigmaX**4 + sigmaY**4 + sigmaZ**4) + 6*(sigmaX**2 * sigmaY**2 + sigmaY**2 * sigmaZ**2 + sigmaZ**2 * sigmaX**2)
    denominator = (S.var()**0.5)**4
    ExS = (numerator/denominator) - 3
    print(rrstr(ExS,3),'эксцесс Ex(S)')
    '''
    return [task,answer]
def SDRV_3():
    task='''
        Монеты в количестве 11
    штук подбрасываются до тех пор, пока 14 раз не выпадет 5
    гербов. Пусть X
    – число бросков до первого появления 5
    гербов, а Y
    – число бросков до последнего появления 5
    гербов (Y
    = общее число бросков). Найдите:

    1) математическое ожидание X
    ;

    2) стандартное отклонение X
    ;

    3) коэффициент корреляции между X
    и Y
    ;

    4) математическое ожидание XY
    .
    '''
    answer ='''
    def C(n,k):
        return math.comb(n,k)

    #Дано
    N = 11
    n = 14
    G = 5

    M = geom(1/2 ** N * C(N,G))

    #1
    print(rrstr(M.mean(),3),'Математическое ожидание X')
    #2
    print(rrstr((M.var())**0.5,3),'Стандартное отклонение X')
    #3
    print(rrstr(M.var()/(M.std() * (n*M.var())**0.5),3),'Коэффициент корреляции X и Y')
    #4
    print(rrstr(M.var()+n*M.mean()**2,1),'Математическое ожидание XY')

    '''
    return [task,answer]
def SDRV_4():
    task='''
    Корзина содержит 34
    шаров, среди которых 14
    – красных и 5
    – синих. Из корзины, случайным образом, без возвращения извлекаются 12
    шаров. Пусть X
    и Y
    обозначают количество красных и синих шаров среди извлеченных, соответственно. Найдите ковариацию Cov(X,Y)
    .
    '''
    answer ='''
    X = 14
    Y = 5
    N = 34
    n = 12

    Ex = X/N * n
    Ey = Y/N * n
    Z = N - X - Y

    def C(n,k):
        return math.comb(n,k)


    dXY = dict()
    for i in range(X+1):
        for j in range(Y+1):
            for k in range(Z+1):
                if (i+j+k)==n:
                    p = C(X,i)*C(Y,j)*C(Z,k)/C(N,n)
                    dXY.setdefault(i*j,0)
                    dXY[i*j]+=p

    val = [i for i in dXY.keys()]
    chn = [i for i in dXY.values()]
    Exy = rv_discrete(values=(val,chn)).mean()
    print(rrstr(Exy - Ex*Ey,2))
    '''
    return [task,answer]

#ConditionalCharacteristicsOfEvents
def CCE_1():
    task='''
    Несимметричная игральная кость подбрасывается до тех пор, пока не выпадут цифры $4$ и $5$. Пусть $X$ — число сделанных при этом бросков. Даны вероятности появления цифр в одном броске: $\mathbb{P}(4)=0,11$ и $\mathbb{P}(5)=0,22$.Требуется найти: 1) $\mathbb{E}(X)$; 2)$\mathbb{Var}(X)$, если известно, что из 4 и 5 сначала выпала цифра 5
    '''
    answer ='''
    a = 0.11
    b = 0.22

    #исходя из вычислений ниже
    ex = 1/a+1/b-1/(a+b)
    varx=(1-a-b)/(a+b)**2+(1-a)/a**2#b->a

    rrstr(ex,4), rrstr(varx,3)
    '''
    return [task,answer]
def CCE_2():
    task='''
    Несимметричная игральная кость подбрасывается до тех пор, пока не выпадут цифры $1, 2$ и $4$. Пусть $X$ — число сделанных при этом бросков. Даны вероятности появления цифр в одном броске: $P(1)=0,14, P(2)=0,19$ и $P(4)=0,13$. Требуется найти:
    1. $\mathbb{E}(X)$
    2. $\mathbb{Var}(X)$, если известно, что из $1, 2$ и $4$ сначала выпала цифра $1$, затем — $2$
    '''
    answer ='''
    a=0.14
    b=0.19
    c=0.13

    #исходя из вычислений ниже

    ex = (1+a/(b+c)+b/(a+c)+c/(a+b)+a*b/(c*(b+c))+a*b/(c*(a+c))+a*c/(b*(b+c))+a*c/(b*(b+a))+c*b/(a*(b+a))+c*b/(a*(c+a)))/(a+b+c)
    var =(1-a-b-c)/(a+b+c)**2+(1-b-c)/(b+c)**2+(1-c)/c**2 #при a->b->c

    rrstr(ex,3),rrstr(var,3)
    '''
    return [task,answer]

#ApproximateCalculationByMonteCarloMethod
def ACMK_1():
    task='''
    В прямоугольной области, заданной ограничениями |x|⩽20
    и |y|⩽8
    , случайным образом выбираются две точки: (x1,y1)
    и (x2,y2)
    . Пусть A
    и B
    – события, состоящие в том, что: A
    – расстояние между выбранными точками меньше 11; B
    – модуль разности |x1−x2|
    меньше 14. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A)
    ; 2) условную вероятность P(A|B)
    . Указание: получите в заданной прямоугольной области 100000 пар точек и, используя все эти точки, найдите ответы, округляя их до одного знака после запятой.
    '''
    answer ='''
    # Вероятность P(A)
    a=20
    b=8
    le1=11
    le2=14

    X = uniform(0, 2*a)
    Y = uniform(0, 2*b)
    N = 100_000
    count = 0
    for i in range(N):
        x1 = X.rvs(size=1)[0]
        y1 = Y.rvs(size=1)[0]
        x2 = X.rvs(size=1)[0]
        y2 = Y.rvs(size=1)[0]
        if ((x2 - x1)**2 + (y2 - y1)**2)**0.5 < le1:
            count += 1

    print(count/N)
    
    # Вероятность P(A|B)
    X = uniform(0, 2*a)
    Y = uniform(0, 2*b)
    N = 100_000
    count1 = 0
    count2 = 0
    for i in range(N):
        x1 = X.rvs(size=1)[0]
        y1 = Y.rvs(size=1)[0]
        x2 = X.rvs(size=1)[0]
        y2 = Y.rvs(size=1)[0]
        if ((x2 - x1)**2 + (y2 - y1)**2)**0.5 < le1 and abs(x2 - x1) < le2:
            count1 += 1
        if abs(x2 - x1) < 14:
            count2 += 1

    print(count1/count2)
    '''
    return [task,answer]
def ACMK_2():
    task='''
        В области, ограниченной эллипсом (u/13)^2+(v/6)^2=1
    , случайным образом выбираются две точки. Пусть A
    и B
    – события, состоящие в том, что: A
    – расстояние между выбранными точками меньше 7,9; B
    – все координаты обеих точек больше 0. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A)
    ; 2) условную вероятность P(A|B)
    . Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.
    '''
    answer ='''
    # Вероятность P(A)

    U = uniform(0, 26)
    V = uniform(0, 12)
    N = 100_000
    count = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-13)**2/169 + (y-6)**2/36 < 1:
            points.append((x, y))


    for i in range(N):
        point_1 = random.choice(points)
        point_2 = random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < 7.9:
            count += 1

    print(count/N)
    
    # Вероятность P(A|B)

    U = uniform(0, 26)
    V = uniform(0, 12)
    N = 100_000
    count1 = 0
    count2 = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-13)**2/169 + (y-6)**2/36 < 1:
            points.append((x, y))

    for i in range(N):
        point_1 = random.choice(points)
        point_2 = random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < 7.9\
        and point_1[0] > 13 and point_2[0] > 13 and point_1[1] > 6 and point_2[1] > 6:
            count1 += 1
        if point_1[0] > 13 and point_2[0] > 13 and point_1[1] > 6 and point_2[1] > 6:
            count2 += 1

    print(count1/count2)
    '''
    return [task,answer]
def ACMK_3():
    task='''
        В области, ограниченной эллипсом (u/23)^2+(v/6)^2=1
    , случайным образом выбираются две точки. Пусть A
    и B
    – события, состоящие в том, что: A
    – расстояние между выбранными точками меньше 9,2; B
    – координаты первой точки больше 0, а координаты второй точки меньше 0. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A)
    ; 2) условную вероятность P(A|B)
    . Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.
    '''
    answer ='''
    # Вероятность P(A)

    U = uniform(0, 46)
    V = uniform(0, 12)
    N = 100_000
    count = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-23)**2/529 + (y-6)**2/36 <= 1:
            points.append((x, y))


    for i in range(N):
        point_1 = random.choice(points)
        point_2 = random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < 9.2:
            count += 1

    print(count/N)
    # Вероятность P(A|B)

    U = uniform(0, 46)
    V = uniform(0, 12)
    N = 100_000
    count1 = 0
    count2 = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-23)**2/529 + (y-6)**2/36 < 1:
            points.append((x, y))


    for i in range(N):
        point_1 = random.choice(points)
        point_2 = random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < 9.2\
        and (point_1[0] > 23 and point_2[0] < 23 and point_1[1] > 6 and point_2[1] < 6\
        or point_1[0] < 23 and point_2[0] > 23 and point_1[1] < 6 and point_2[1] > 6):
            count1 += 1
        if point_1[0] > 23 and point_2[0] < 23 and point_1[1] > 6 and point_2[1] < 6\
        or point_1[0] < 23 and point_2[0] > 23 and point_1[1] < 6 and point_2[1] > 6:
            count2 += 1

    print(count1/count2)
    '''
    return [task,answer]
def ACMK_4():
    task='''
        В кубе объема 1 случайным образом выбираются точки A
    , B
    и C
    . Пусть R
    , S
    и T
    – события, состоящие в том, что: R
    – наименьший угол в треугольнике ABC
    меньше 26,7°; S
    – наибольший угол в треугольнике ABC
    меньше 81,9°; T
    – треугольник ABC
    остроугольный. Найдите приближенно, методом Монте-Карло: 1) условную вероятность P(R|T)
    ; 2) условную вероятность P(S|T)
    . Указание: получите 100000 остроугольных треугольников ABC
    и, используя все эти треугольники, найдите ответы, округляя их до одного знака после запятой.
    '''
    answer ='''
    X = uniform()
    Y = uniform()
    Z = uniform()
    N = 100_000
    count1 = 0
    count2 = 0
    count3 = 0

    for i in range(N):
        A = X.rvs(size = 3)
        B = Y.rvs(size = 3)
        C = Z.rvs(size = 3)
        AB = ((B[0]-A[0])**2 + (B[1]-A[1])**2 + (B[2]-A[2])**2)**0.5
        AC = ((C[0]-A[0])**2 + (C[1]-A[1])**2 + (C[2]-A[2])**2)**0.5
        BC = ((C[0]-B[0])**2 + (C[1]-B[1])**2 + (C[2]-B[2])**2)**0.5
        min_side = min(AB, AC, BC)
        med_side = AB + BC + AC - max(AB, AC, BC) - min(AB, AC, BC)
        max_side = max(AB, AC, BC)
        min_angle = math.degrees(math.acos((max_side**2 + med_side**2 - min_side**2)/(2 * med_side * max_side)))
        max_angle = math.degrees(math.acos((min_side**2 + med_side**2 - max_side**2)/(2 * med_side * min_side)))
        check_traingle = min_side**2 + med_side**2 > max_side**2

        # Вероятность P(T)

        if check_traingle:
            count1 += 1

        # Вероятность P(R*T)

        if check_traingle and min_angle < 26.7:
            count2 += 1

        # Вероятность P(S*T)

        if check_traingle and max_angle < 81.9:
            count3 += 1

    PRT = count2/count1
    PST = count3/count1
    PRT, PST
    '''
    return [task,answer]

def PAN_1():

    task ='''
        Математическое ожидание доходности акций компаний А и В составляет $3$% и $4$%, 
    при этом стандартное отклонение доходности равно $4$% и $7$%, соответственно. Также известен 
    коэффициент корреляции $\rho_{AB}$ доходностей акций А и В, $\rho_{AB}=0,47$. Найдите (короткие позиции допускаются):
    1) доли акций А и В в портфеле с минимальной дисперсией доходности;
    2) ожидаемую доходность и стандартное отклонение доходности такого портфеля.
    '''
    answer ='''
muA, muB = 0.03, 0.04
sigmaA, sigmaB = 0.04, 0.07

roAB = 0.47

a = (sigmaB**2 - roAB*sigmaA*sigmaB) / (sigmaA**2 + sigmaB**2 - 2*roAB*sigmaA*sigmaB)
b = 1-a
muR = a*muA + b*muB
VarR = (a**2)*(sigmaA**2) + (b**2)*(sigmaB**2) + 2*a*b*roAB*sigmaA*sigmaB

rrstr(a, 2), rrstr(b, 2),rrstr(muR*100, 1),rrstr((VarR**0.5)*100, 2)
    '''
    return [task,answer]

def ft5_4_1():
    task='''
    Случайный вектор(X,Y) равномерно распределен в треугольнике x⩾0, y⩾0, 52x+y⩽52.Найдите математическое ожидание E(X^10Y).'''
    answer='''
x,y = symbols('x y',real=True)

f = 1/integrate(1,(y,0,33-33*x),(x,0,1))

EX10Y = integrate(f* x**10 * y,(y,0,33-33*x),(x,0,1))
EX10Y    
    '''
    return [task,answer]

def ft5_4_2():
    task='''Случайный вектор имеет плотность распределения f(x,y) =1/2 x + C y , 0<x<1, 0<y<2, найдите константу C и вероятность P(X+Y>1)'''
    answer='''
x, y, C = sp.symbols('x y C')
 
f = 1 / 2 * x + C*y
 
i = sp.integrate(f, (y, 0, 2), (x, 0, 1))
 
c0 = sp.solve(i - 1)[0]
f = f.subs(C, c0)
display(C0)
sp.integrate(f, (y, -x+1, 2), (x, 0, 1))
    '''
    return [task,answer]
def ft5_4_3():
    task='''
Случайный вектор (X,Y) имеет плотность распределения f(x,y)= 12e^(−4x−3y), если 0⩽x<+∞, 0⩽y<+∞, 0, в остальных точках. Найдите вероятность P(X<2).    
    '''
    answer='''
from sympy import *
x, y = symbols('x y')
f = 12*exp(-3*x-4*y)
integrate(f,(y,0,'oo'),(x,1,'oo'))    
    '''
    return [task,answer]
def ft5_5():
    task='''
Плотность распределения случайного вектора (X,Y) имеет вид: f_X,Y(x,y)= 1/π *e^(−5/2 * x^2−18x−36−xy−6y−1/2 * y^2) . Найдите условное математическое ожидание E(Y|X=x).    
    '''
    answer='''
import sympy
#после выноса -1/2!!!!!!
coefs = {
            'x^2': 5,
            'x': 36,
            'xy': 2,
            'y': 12,
            'y^2': 1,
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

print(f'EX_Y = {EX_Y},\nEY_X = {EY_X},\nVarX_Y = {VarX_Y},\nVarY_X = {VarY_X},\nEX = {sol[EX]},\nEY = {sol[EY]},\nVarX = {VarX},\nVarY = {VarY},\nCovXY = {CovXY},\nroXY = {roXY}')    
    '''
    return [task,answer]
    

def describe_text():
    t="import pandas as pd\n\
    import matplotlib.pyplot as plt\n\
    import numpy as np\n\
    import scipy.stats\n\
    from statsmodels.distributions.empirical_distribution import ECDF\n\
    \n\
    def from_big_text(data:str,splitter:str):\n\
        \n\
        index = pd.Index('''Объем выборки до удаления пропущенных данных\n\
    Количество пропущенных данных (NA)\n\
    Объем выборки после удаления пропущенных данных\n\
    Минимальное значение в вариационном ряду\n\
    Максимальное значение в вариационном ряду\n\
    Размах выборки\n\
    Значение первой квартили (Q1)\n\
    Значение медианы (Q2)\n\
    Значение третьей квартили (Q3)\n\
    Квартильный размах\n\
    Среднее выборочное значение\n\
    Стандартное отклонение (S) корень из дисп.в (исправленной)\n\
    Исправленная дисперсия \n\
    Эксцесс\n\
    Коэффициент асимметрии\n\
    Ошибка выборки\n\
    Значение 63%-квантили\n\
    Мода\n\
    Как часто встречается 'мода'\n\
    Верхняя граница нормы (Xst_max)\n\
    Нижняя граница нормы (Xst_min)\n\
    Количество выбросов ниже нижней нормы\n\
    Количество выбросов выше верхней нормы\n\
    '''.split('\n'))\n\
    \n\
    data_list=[]\n\
    df=pd.DataFrame([float(i) if i!='NA' and i!='-NA' else np.nan for i in data.split(splitter)])\n\
    \n\
    length_before=df.size\n\
    data_list.append(length_before)\n\
    \n\
    df=df.dropna()\n\
    length_after=df.size\n\
    data_list.extend([length_after-length_before,length_after])\n\
    \n\
    minn=df.describe().loc['min'].values[0]\n\
    maxx=df.describe().loc['max'].values[0]\n\
    data_list.extend([minn,maxx,maxx-minn])\n\
    \n\
    Q1=df.describe().loc['25%'].values[0]\n\
    Q2=df.describe().loc['50%'].values[0]\n\
    Q3=df.describe().loc['75%'].values[0]\n\
    \n\
    mean = df.describe().loc['mean'].values[0]\n\
    \n\
    data_list.extend([Q1,Q2,Q3,Q3-Q1,mean,df.std(ddof=1)[0],df.var(ddof=1)[0],df.kurt()[0],df.skew()[0]])\n\
    \n\
    data_list.append(data_list[11]/data_list[2]**0.5)\n\
    data_list.extend(df.quantile(0.63))\n\
    \n\
    if df.mode().count()[0] == df.count().iloc[0]:\n\
        data_list.append(0)\n\
        data_list.append(0)\n\
    else:\n\
        data_list.append(df.mode().iloc[0,0])\n\
        data_list.append(df.value_counts()[df.mode().iloc[0,0]])\n\
    \n\
    data_list.extend([data_list[8]+1.5*data_list[9],data_list[6]-1.5*data_list[9]])\n\
    data_list.extend([len(df[df.iloc[:,0]<data_list[20]]),len(df[df.iloc[:,0]>data_list[19]])])\n\
    \n\
    df.boxplot()\n\
    plt.xlabel('Ящик с усами до очистки')\n\
    plt.show()\n\
    \n\
    clean_df=df[(df.iloc[:,0]>data_list[20]) & (df.iloc[:,0]<data_list[19])]\n\
    clean_df.boxplot()\n\
    plt.xlabel('Ящик с усами после очистки (Без NA и выбросов)')\n\
    plt.show()\n\
    \n\
    \n\
    return pd.DataFrame(data_list,index[:len(data_list)])"
    
    return t


themes = {'Непрерывные случайные величины': ['CRV_1()',CRV_1()[0],'CRV_2()',CRV_2()[0]],
              'Нормальные случайные векторы': ['NRV_1()',NRV_1()[0], 'NRV_2()',NRV_2()[0],'NRV_3()', NRV_3()[0]],
              'Формулы полной вероятности и Байеса':['FPB_1()',FPB_1()[0],'FPB_2()',FPB_2()[0],'FPB_3()',FPB_3()[0],'FPB_4()',FPB_4()[0]],
              'Специальные дискретные случайные величины':['SDRV_1()',SDRV_1()[0],'SDRV_2()',SDRV_2()[0],'SDRV_3()',SDRV_3()[0],'SDRV_4()',SDRV_4()[0]],
              'Условные характеристики относительно группы событий':['CCE_1()',CCE_1()[0],'CCE_2()',CCE_2()[0]],
              'Приближенное вычисление вероятности методом Монте-Карло':['ACMK_1()',ACMK_1()[0],'ACMK_2()',ACMK_2()[0],'ACMK_3()',ACMK_3()[0],'ACMK_4()',ACMK_4()[0]],
              'Портфельный анализ': ['PAN_1()',PAN_1()[0]],
              'Для теста 5': ['ft5_4_1()',ft5_4_1()[0],'ft5_4_2()',ft5_4_2()[0],'ft5_4_3()',ft5_4_3()[0], 'ft5_5()',ft5_5()[0]],
              'Включить функцию для добавления в буфер обмена': ['enable_ppc'],
              'Описательная статистика': ['describe_text()']
              }

def description(dict_to_show = themes, show_only_keys:bool = False,show_tasks=True):
    if show_only_keys==True:
        show_tasks=False
    text = ""
    length1=1+max([len(x) for x in list(dict_to_show.keys())])
    for key in dict_to_show.keys():
        text += f'{key:^{length1}}'
        if not show_only_keys and show_tasks:
            text +=': \n\n'
            for f in dict_to_show[key]:
                text += f'{f};\n\n'
        elif not show_only_keys and not show_tasks:
            text +=': '
            for f in dict_to_show[key]:
                text += f'{f};\n'+' '*(length1+2)
            text += '\n'
        else:
            text += '\n'
    print(text)