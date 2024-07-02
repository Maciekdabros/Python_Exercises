import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def mass_spring_dynamics(t, state, m, c, k, A, f):
    """
    Oblicza pochodne dla układu masy na sprężynie z zewnętrznym wymuszeniem.

    Parameters:
    t : float
        Aktualny czas w symulacji.
    state : list or ndarray
        Aktualny stan układu, gdzie state[0] to przemieszczenie (x) i state[1] to prędkość (v).
    m : float
        Masa obiektu.
    c : float
        Współczynnik tłumienia.
    k : float
        Współczynnik sztywności sprężyny.
    A : float
        Amplituda siły zewnętrznej.
    f : float
        Częstotliwość siły zewnętrznej.
    Returns:
    list: Pochodne dxdt (prędkość) i dvdt (przyspieszenie).
    """
    x, v = state
    dxdt = v
    dvdt = (A * np.sin(2 * np.pi * f * t) - c * v - k * x) / m
    return [dxdt, dvdt]

def run_simulation(m_f_pair):
    """
    Uruchamia symulację dla danego zestawu parametrów masy i częstotliwości.

    Parameters:
    m_f_pair : tuple
        Para wartości (m, f), gdzie m to masa, a f to częstotliwość.

    Returns:
    float: Maksymalne przemieszczenie dla danej pary parametrów.
    """
    m, f = m_f_pair
    sol = solve_ivp(mass_spring_dynamics, [0, simulation_time], initial_conditions,
                    args=(m, c, k, A, f), t_eval=t_eval, method='RK45')
    return np.max(np.abs(sol.y[0]))


def multithreading_simulation():
    """
    Uruchamia symulacje wielowątkowe dla wszystkich par masy i częstotliwości.

    Returns:
    ndarray: Macierz maksymalnych przemieszczeń dla każdej pary parametrów.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(run_simulation, zip(np.ravel(M), np.ravel(F))))
    return np.array(results).reshape(M.shape)


def multiprocessing_simulation():
    """
    Uruchamia symulacje wieloprocesowe dla wszystkich par masy i częstotliwości.

    Returns:
    ndarray: Macierz maksymalnych przemieszczeń dla każdej pary parametrów.
    """
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_simulation, zip(np.ravel(M), np.ravel(F))))
    return np.array(results).reshape(M.shape)

    
c = 0.001
k = 1000
A = 1
simulation_time = 10
time_step = 0.01
t_eval = np.arange(0, simulation_time, time_step)

initial_conditions = [0, 0]

mass_values = np.linspace(1, 10, 30)
frequency_values = np.linspace(1, 10, 30)
M, F = np.meshgrid(mass_values, frequency_values)

if __name__ == "__main__":
    #sequential
    start_time = time.time()
    sequential_max_displacements = np.array([run_simulation(m_f) for m_f in zip(np.ravel(M), np.ravel(F))]).reshape(M.shape)
    elapsed_time_sequential = time.time() - start_time
    print(f"Sequential simulation took {elapsed_time_sequential:.2f} seconds.")

    #multithreading
    start_time = time.time()
    threaded_max_displacements = multithreading_simulation()
    elapsed_time_threaded = time.time() - start_time
    print(f"Multithreaded simulation took {elapsed_time_threaded:.2f} seconds.")

    #multiprocessing
    start_time = time.time()
    multiprocessed_max_displacements = multiprocessing_simulation()
    elapsed_time_multiprocessed = time.time() - start_time
    print(f"Multiprocessing simulation took {elapsed_time_multiprocessed:.2f} seconds.")

    # Porównanie wyników
    are_sequential_and_threaded_equal = np.allclose(sequential_max_displacements, threaded_max_displacements)
    print(f"Sequential and multithreaded results are equal: {are_sequential_and_threaded_equal}")

    are_sequential_and_multiprocessed_equal = np.allclose(sequential_max_displacements, multiprocessed_max_displacements)
    print(f"Sequential and multiprocessing results are equal: {are_sequential_and_multiprocessed_equal}")

    #plot
    plt.figure(figsize=(12, 8))
    pcolor = plt.pcolormesh(F, M, sequential_max_displacements, shading='auto')
    plt.colorbar(pcolor, label='Maksymalne przemieszczenie [m]')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Masa [kg]')
    plt.title('Charakterystyki częstotliwościowe w zależności od masy i częstotliwości')
    plt.show()
