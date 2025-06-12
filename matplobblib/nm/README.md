# Модуль `nm`

Этот модуль содержит набор подмодулей для выполнения различных численных методов, включая решение уравнений, оптимизацию, линейную алгебру, интерполяцию и другие.

## Подмодули

### 1. [additional_funcs](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/additional_funcs#readme)

Этот модуль  предоставляет набор вспомогательных функций для работы с числовыми данными, включая:

- Генерацию массивов с возмущениями (`generate_perturbed_array`).
- Интерполяцию для восстановления пропусков в данных (`quadratic_interpolate`).
- Вычисление ближайшей степени двойки (`next_power_of_two`).
- Дополнение матриц нулями (`pad_matrix`).
- Поиск максимального внедиагонального элемента в симметричной матрице (`parallel_max_offdiag`).
- Поиск ближайших соседей на основе косинусного сходства (`nearest_cosine_neighbors`).

### 2. [base](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/base#readme)

Этот модуль  содержит функции для демонстрации и анализа различных аспектов численных вычислений, таких как:

- Переполнение (`perepolnenie`).
- Потеря точности (`poterya_tochnosti`).
- Ошибки округления (`oshibka_okrugleniya`).
- Накопление ошибок (`nakoplenie_oshibok`).
- Потеря значимости (`poterya_znachimosti`).
- Алгоритм суммирования по Кохану для минимизации ошибок округления (`summirovanie_po_Kohanu`).

### 3. [differential_eqs](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/differential_eqs#readme)

Этот модуль  предоставляет функции для численного решения обыкновенных дифференциальных уравнений (ОДУ) и систем ОДУ, включая:

- Метод Эйлера для решения ОДУ (`euler_method`).
- Визуализацию решений ОДУ для разных шагов интегрирования (`plot_euler_solutions`).
- Метод Эйлера для решения систем ОДУ (`euler_system`).
- Построение фазовых портретов систем ОДУ (`plot_phase_portrait_with_streamplot`, `plot_phase_portrait_3d`, `plot_phase_portrait_4d`).
- Решение систем ОДУ с задержкой (`euler_delay_system`).

### 4. [eigen](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/eigen#readme)

Этот модуль содержит подмодули для вычисления собственных значений и собственных векторов матриц:

- `jacobi`: Реализует метод Якоби (базовый, Numba-оптимизированный и параллельный).
- `qr`: Содержит QR-алгоритм (базовый и со сдвигами).
- `vectors_from_values`: Функции для вычисления собственных векторов по заданным собственным значениям и построения ортонормированного базиса.

### 5. [eqs](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/eqs#readme)

Этот модуль предоставляет численные методы для решения нелинейных уравнений и задач оптимизации, включая:

- Методы поиска корней (бисекция, Ньютона, секущих, Вегстейна, простой итерации).
- Метод поиска минимума функции (дихотомия).

### 6. [interp](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/interp#readme)

Этот модуль  предоставляет функции для интерполяции данных:

- Полиномиальная интерполяция Лагранжа (`lagrange_interpolation`, `lagrange_interpolation_func_get`).
- Линейная интерполяция для работы с временными задержками (`get_delayed_value`).

### 7. [matrices](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/matrices#readme)

Этот модульпредоставляет функции для работы с матрицами и векторами, оптимизированные с помощью Numba, включая:

- Скалярное произведение, вычисление нормы.
- Арифметические операции с векторами и матрицами.
- Транспонирование, создание и инвертирование диагональных матриц.
- LU- и QR-разложения.

### 8. [sistems](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/sistems#readme)

Этот модуль предоставляет методы решения систем уравнений:

- Метод простой итерации (`simple_iteration_system`, `simple_iteration_system_no_np`).
- Метод Зейделя (`seidel_method`).
- Метод Ньютона для систем 2x2 (`newton_system`).
- Метод Гаусса (с Numba) (`solve_gauss_njit`).

### 9. [strassen](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/strassen#readme)

Этот модуль содержит реализации алгоритма умножения матриц Штрассена, включая оптимизированные версии с использованием Numba.

### 10. [fourier](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm/fourier#readme)

Преобразование Фурье и спектральный анализ: Дискретное DFT, Обратное IDFT, Быстрое FFT