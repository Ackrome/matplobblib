from  inspect import getsource
from .FPB import *                      # Формулы полной вероятности и Байеса
from .SDRV import *                     # Специальные дискретные случайные величины
from .CRV import *                      # Непрерывные случайные величины
from .NRV import *                      # Нормальные случайные векторы
from .describe_text import *            # Описательная статистика

def imports():
    return '''
    
    from scipy.integrate import quad
    import math
    import numpy a np
    import sympy
    import itertools
    sympy.init_printing(use_unicode=True,use_latex=True)
    '''
    
def enable_ppc():
    return'''
import pyperclip

#Делаем функцию которая принимает переменную text
def write(name):
    pyperclip.copy(name) #Копирует в буфер обмена информацию
    pyperclip.paste()'''

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

themes = {    'Непрерывные случайные величины': ['CRV_1()','CRV_2()'],
              'Нормальные случайные векторы': ['NRV_1()', 'NRV_2()','NRV_3()'],
              'Формулы полной вероятности и Байеса':['FPB_1()','FPB_2()','FPB_3()','FPB_4()'],
              'Специальные дискретные случайные величины':['SDRV_1()','SDRV_2()','SDRV_3()','SDRV_4()'],
              'Условные характеристики относительно группы событий':['CCE_1()','CCE_2()'],
              'Приближенное вычисление вероятности методом Монте-Карло':['ACMK_1()','ACMK_2()','ACMK_3()','ACMK_4()'],
              'Портфельный анализ': ['PAN_1()'],
              'Для теста 5': ['ft5_4_1()','ft5_4_2()','ft5_4_3()', 'ft5_5()'],
              'Включить функцию для добавления в буфер обмена': ['enable_ppc'],
              'Описательная статистика': ['describe_text()']
              }

def description(dict_to_show = themes, show_only_keys:bool = False,show_tasks=True):
    if show_only_keys==True:
        show_tasks=False
    text = ""
    text+='Чтобы узнать код функции воспользуйтесь функцией `getsource()` от нужной функции.\n Так, например, можно вывести код функции `describe_text`\n'
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