import numpy as np
import time
import random

def function(x):
    """
    Funkcja kwadratowa.

    Args:
    x (float): Wartość, dla której funkcja ma być obliczona.

    Returns:
    float: Wynik funkcji kwadratowej x^2.
    """
    return x**2

def monte_carlo_integration_pure_python(func, a, b, points):
    """
    Oblicza całkę oznaczoną funkcji metodą Monte Carlo używając czystego Pythona.

    Args:
    func (function): Funkcja, której całkę chcemy obliczyć.
    a (float): Dolna granica przedziału całkowania.
    b (float): Górna granica przedziału całkowania.
    points (int): Liczba punktów do wygenerowania dla aproksymacji.

    Returns:
    float: Przybliżona wartość całki oznaczonej funkcji.
    """
    count_under_curve = 0
    for i in range(points):
        x = random.uniform(a, b)
        y = random.uniform(0, func(b))
        if y <= func(x):
            count_under_curve += 1
    area = (b - a) * func(b)
    integral = area * (count_under_curve / points)
    return integral

def monte_carlo_integration_numpy(func, a, b, points):
    """
    Oblicza całkę oznaczoną funkcji metodą Monte Carlo używając biblioteki NumPy.

    Args:
    func (function): Funkcja, której całkę chcemy obliczyć.
    a (float): Dolna granica przedziału całkowania.
    b (float): Górna granica przedziału całkowania.
    points (int): Liczba punktów do wygenerowania dla aproksymacji.

    Returns:
    float: Przybliżona wartość całki oznaczonej funkcji.
    """
    xs = np.random.uniform(a, b, points)
    ys = np.random.uniform(0, func(b), points)
    count_under_curve = np.sum(ys <= func(xs))
    area = (b - a) * (func(b))
    integral = area * (count_under_curve / points)
    return integral

def main():
    a = 0
    b = 2
    points = 10000000

    start_time_python = time.time()
    integral_pure_python = monte_carlo_integration_pure_python(function, a, b, points)
    end_time_python = time.time()

    start_time_numpy = time.time()
    integral_numpy = monte_carlo_integration_numpy(function, a, b, points)
    end_time_numpy = time.time()

    print(f"Całka bez numpy: {integral_pure_python}, Czas: {end_time_python - start_time_python} sekund")
    print(f"Całka z numpy: {integral_numpy}, Czas: {end_time_numpy - start_time_numpy} sekund")

if __name__ == "__main__":
    main()