from .rrstr import *
#######################################################################################################################
# Приближенное вычисление вероятности методом Монте-Карло
#######################################################################################################################
def ACMK_1(a,b,le1,le2):
    """В прямоугольной области, заданной ограничениями |x| ⩽ `a` и |y| ⩽ `b`,
    случайным образом выбираются две точки: (x1,y1) и (x2,y2).
    Пусть A и B - события, состоящие в том, что: 
    A - расстояние между выбранными точками меньше `le1`;
    B - модуль разности |x1 - x2| меньше `le2`.
    Найдите приближенно, методом Монте-Карло:
    - вероятность P(A)
    - условную вероятность P(A|B)
    Указание: получите в заданной прямоугольной области 100000 пар точек и, используя все эти точки, найдите ответы, округляя их до одного знака после запятой.

    Args:
        a (numerical): Значение меньше которого модуль X
        b (numerical): Значение меньше которого модуль Y
        le1 (numerical): Число из первого(A) условия
        le2 (numerical): Число из второго(B) условия

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    import scipy.stats
    
    # Вероятность P(A)
    X = scipy.stats.uniform(0, 2*a)
    Y = scipy.stats.uniform(0, 2*b)
    N = 100_000
    count = 0
    for i in range(N):
        x1 = X.rvs(size=1)[0]
        y1 = Y.rvs(size=1)[0]
        x2 = X.rvs(size=1)[0]
        y2 = Y.rvs(size=1)[0]
        if ((x2 - x1)**2 + (y2 - y1)**2)**0.5 < le1:
            count += 1
            
    answer = [count/N]
    print('Вероятность P(A) = ' + rrstr(answer[0],1))
    
    # Вероятность P(A|B)
    X = scipy.stats.uniform(0, 2*a)
    Y = scipy.stats.uniform(0, 2*b)
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
            
    answer.append(count1/count2)
    print('Условную вероятность P(A|B) = ' + rrstr(answer[1],1))
    
    answer = tuple(answer)
    return answer
#######################################################################################################################
def ACMK_2(a,b,le,sign):
    """В области, ограниченной эллипсом (u/`a`)^2+(v/`b`)^2=1,
    случайным образом выбираются две точки.
    Пусть A и B – события, состоящие в том, что:
    A - расстояние между выбранными точками меньше `le`;
    B - все координаты обеих точек `sign` 0. 
    Найдите приближенно, методом Монте-Карло: 
    - вероятность P(A)
    - условную вероятность P(A|B)
    
    Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.

    Args:
        a (numerical): 1-я полуось
        b (numerical): 2-я полуось
        le (numerical): Чтсло из первого условия(A)
        sign (numerical): '>' или '<' чем 0

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    import scipy.stats
    import numpy
    # Вероятность P(A)


    U = scipy.stats.uniform(0, 2*a)
    V = scipy.stats.uniform(0, 2*b)
    N = 100_000
    count = 0
    points = []
    
    signs = {'>':max,'<':min}

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-a)**2/a**2 + (y-b)**2/b**2 < 1:
            points.append((x, y))

    for i in range(N):
        point_1 = numpy.random.choice(points)
        point_2 = numpy.random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < le:
            count += 1

    answer = [count/N]
    
    print('Вероятность P(A) = ' + rrstr(answer[0],1))
    
    # Вероятность P(A|B)

    U = scipy.stats.uniform(0, 2*a)
    V = scipy.stats.uniform(0, 2*b)
    N = 100_000
    count1 = 0
    count2 = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-a)**2/a**2 + (y-b)**2/b**2 < 1:
            points.append((x, y))

    for i in range(N):
        point_1 = numpy.random.choice(points)
        point_2 = numpy.random.choice(points)
        
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < le and signs[sign](point_1[0],a)==point_1[0] and signs[sign](point_2[0], a)==point_2[0] and signs[sign](point_1[1], b)==point_1[1] and signs[sign](point_2[1],b)==point_2[1]:
            count1 += 1
        if signs[sign](point_1[0],a)==point_1[0] and signs[sign](point_2[0], a)==point_2[0] and signs[sign](point_1[1], b)==point_1[1] and signs[sign](point_2[1],b)==point_2[1]:
            count2 += 1
            
    answer.append(count1/count2)
    print('Условную вероятность P(A|B) = ' + rrstr(answer[1],1))
    
    answer = tuple(answer)
    return answer
#######################################################################################################################
def ACMK_3(a,b,le):
    """В области, ограниченной эллипсом (u/`a`)^2+(v/`b`)^2=1,
    случайным образом выбираются две точки.
    Пусть A и B - события, состоящие в том, что: 
    A - расстояние между выбранными точками меньше `le`; 
    B – координаты первой точки больше 0, а координаты второй точки меньше 0.
    Найдите приближенно, методом Монте-Карло: 
    - вероятность P(A)
    - условную вероятность P(A|B)
    
    Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.


    Args:
        a (numerical): 1-я полуось
        b (numerical): 2-я полуось
        le (numerical): Чтсло из первого условия(A)

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    ''''''
    import scipy.stats
    import numpy
    # Вероятность P(A)

    U = scipy.stats.uniform(0, 2*a)
    V = scipy.stats.uniform(0, 2*b)
    N = 100_000
    count = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-a)**2/a**2 + (y-b)**2/b**2 < 1:
            points.append((x, y))

    for i in range(N):
        point_1 = numpy.random.choice(points)
        point_2 = numpy.random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5 < le:
            count += 1

    answer = [count/N]
    
    print('Вероятность P(A) = ' + rrstr(answer[0],1))
    # Вероятность P(A|B)

    U = scipy.stats.uniform(0, 2*a)
    V = scipy.stats.uniform(0, 2*b)
    N = 100_000
    count1 = 0
    count2 = 0
    points = []

    for i in range(N):
        x = U.rvs(size=1)[0]
        y = V.rvs(size=1)[0]
        if (x-a)**2/a**2 + (y-b)**2/b**2 < 1:
            points.append((x, y))


    for i in range(N):
        point_1 = numpy.random.choice(points)
        point_2 = numpy.random.choice(points)
        if ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5\
        and (point_1[0] > a and point_2[0] < a and point_1[1] > b and point_2[1] < b\
        or point_1[0] < a and point_2[0] > a and point_1[1] < b and point_2[1] > b):
            count1 += 1
        if point_1[0] > a and point_2[0] < a and point_1[1] > b and point_2[1] < b\
        or point_1[0] < a and point_2[0] > a and point_1[1] < b and point_2[1] > b:
            count2 += 1

    answer.append(count1/count2)
    print('Условную вероятность P(A|B) = ' + rrstr(answer[1],1))
    
    answer = tuple(answer)
    return answer
#######################################################################################################################
def ACMK_4(cond1,r,cond2,s):
    """В кубе объема `V` случайным образом выбираются точки A, B и C.
    Пусть R, S и T - события, состоящие в том, что:
    R - `cond1` угол в треугольнике ABC меньше `r`°;
    S - `cond2` угол в треугольнике ABC меньше `s`°;
    T - треугольник ABC остроугольный.
    Найдите приближенно, методом Монте-Карло:
    - условную вероятность P(R|T)
    - условную вероятность P(S|T)
    
    Указание: получите 100000 остроугольных треугольников ABC и,
    используя все эти треугольники, найдите ответы, округляя их до одного знака после запятой.

    Args:
        cond1 (str): Параметр условия R из <br> `['наименьший','наибольший','найдется','все']`
        r (numerical): Число градусов из условия R
        cond2 (str): Параметр условия S из <br> `['наименьший','наибольший','найдется','все']`
        s (numerical): Число градусов из условия S
        

    ## Prints
        `answer` каждое значение по очереди.<br>C запятой вместо точки и сокращением до соответствующего количества знаков после запятой

    Returns:
        `answer` (tuple): Соответствующие величины
    """
    import scipy.stats
    import math
            
    
    variants = {
        'наименьший': min,
        'наибольший': max,
        'найдется' : any,
        'все' : all
    }
    
    degs=[r,s]
    v_keys = list(variants.keys())
    
    conds=[cond1,cond2]
    
    X = scipy.stats.uniform()
    Y = scipy.stats.uniform()
    Z = scipy.stats.uniform()
    N = 100_000
    
    count1 = 0
    count23 = [0,0]

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
        med_angle = math.degrees(math.acos((max_side**2 + min_side**2 - med_side**2)/(2 * min_side * max_side)))
        max_angle = math.degrees(math.acos((min_side**2 + med_side**2 - max_side**2)/(2 * med_side * min_side)))
        
        check_traingle = min_side**2 + med_side**2 > max_side**2

        # Вероятность P(T)

        if check_traingle:
            count1 += 1

        # Вероятность P(R*T)
        for c in range(len(conds)):
            if conds[c] in v_keys[:2]:
                if check_traingle and variants[conds[c]]([min_angle,med_angle,max_angle]) < degs[c]:
                    count23[c] += 1
            else:
                if check_traingle and variants[conds[c]]([min_angle < degs[c],med_angle < degs[c],max_angle < degs[c]]) :
                    count23[c] += 1

    PRT = count23[0]/count1
    PST = count23[1]/count1
    
    answer = (PRT, PST)
    
    print('Условная вероятность P(R|T) = ' + rrstr(answer[0],1))
    print('Условная вероятность P(S|T) = ' + rrstr(answer[1],1))

    return answer
#######################################################################################################################
ACMK = [ACMK_1,ACMK_2,ACMK_3,ACMK_4]