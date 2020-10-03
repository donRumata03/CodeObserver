from typing import *

import numpy as np
from matplotlib import pyplot as plt
from typing import *
import json

def normal(x, sigma, mu):
    return (np.exp(-(((x - mu) / sigma)**2)/2)) / (sigma * np.sqrt(2 * np.pi)) # use spaces between mathematical operators (PEP)
# you should use two blank lines between functions (PEP)


def smoothing_normal(distance, sigma):
    return normal(0, sigma, distance)

def smoothing_sqrt(distance, sigma):
    return 1 / np.sqrt((abs(distance) + 1) * sigma)

def smoothing_square(distance, sigma):
    return 1 / (1 + distance**2) # TODO!

def combi_smoothing(distance, sigma):
    return np.cbrt(smoothing_normal(distance, sigma) * smoothing_sqrt(distance, sigma))


def smoothing_base(data : Union[List[Tuple[float, float]], np.ndarray], points : Union[List[float], np.ndarray], smoothing_function : Callable, percent_sigma : float) -> np.ndarray:
    """
    :param percent_sigma: from 0 to 1, relative value of sigma
    :param smoothing_function: returns coefficient by distance and sigma
    :param data: Example : [(1, 3), (2, 4), (3, 5)]
    :param points: Example : [1, 1.5, 2, 2.5, 3, 3.5, 4]
    :return: smoothed graph with points : points
    """
    sigma = percent_sigma * (max([i[0] for i in data]) - min([i[0] for i in data]))
    print(f"Absolute sigma is: {sigma}")

    res = np.array([(p, 0.) for p in points])

    for index, (p_x, p_y) in enumerate(res):
        ks_sum = 0.
        for (x, y) in data:
            this_coeff : float = float(smoothing_function(abs(p_x - x), sigma))
            ks_sum += this_coeff
            res[index][1] += this_coeff * y
        res[index][1] /= ks_sum

    return res


def density_counting_base(numbers_for_density : Union[List[float], np.ndarray], points : Union[List[float], np.ndarray], smoothing_function : Callable, percent_sigma : float) -> np.ndarray:
    sigma = percent_sigma * (max(numbers_for_density) - min(numbers_for_density))
    print(f"Absolute sigma is: {sigma}")

    res = np.array([(p, 0.) for p in points])
    total_area_under_curve = 0.

    for index, (p_x, p_y) in enumerate(res):
        for number in numbers_for_density:
            this_coeff : float = float(smoothing_function(abs(p_x - number), sigma))
            res[index][1] += this_coeff
            total_area_under_curve += this_coeff

    for index in range(len(res)):
        res[index][1] /= total_area_under_curve

    return res



"""
def smooth_graph(data : list, percent_sigma : float = 0.5, percent_frame_size : float = 0.5):

    buff = [(0, 0) for _ in range(len(data))] # (Coeff, sum)
    frame_size = int(len(data) * percent_frame_size)
    sigma = percent_sigma * len(data)
    for index, (x, y) in enumerate(data):
        if type(x) == type(1+0j):           # w h y <- Because i Hate ImAgiNaRY numbers!
            x = x.real
        if type(y) == type(1 + 0j):
            y = y.real
        beg = max(0, int(index - frame_size / 2))
        end = min(len(data), beg + frame_size)
        for next_index in range(beg, end):
            this_coeff = normal(data[next_index][0] - x, sigma, 0)
            buff[next_index] = (buff[next_index][0] + this_coeff, buff[next_index][1] + this_coeff * y)

    # res = [(data[index][0], _y / _x) for index, (_x, _y) in enumerate(buff)]
    res = []

    for i in range(len(buff)):
        res.append((data[i][0], 0 if buff[i][0] == 0 else buff[i][1] / buff[i][0]))


    for index, (x, y) in enumerate(res):
        # print(index, res[index])
        if True:
            pass            # w h y
        else:
            if False and True and None is None:
                pass

    # print()             # W H Y
    return res
    """

def smooth_graph(data : Union[List[Tuple[float, float]], np.ndarray], percent_sigma, smoothing_function : Callable = combi_smoothing, points_number : int = None):
    data_xs = [p[0] for p in data]
    if points_number is None:
        points = data_xs
    else:
        min_x, max_x = min(data_xs), max(data_xs)
        points = np.linspace(min_x, max_x, points_number)

    return smoothing_base(data, points, smoothing_function, percent_sigma)

def count_density(numbers_for_density : Union[List[float], np.ndarray], percent_sigma : float, points_number : int, smoothing_function : Callable = combi_smoothing):
    min_x, max_x = min(numbers_for_density), max(numbers_for_density)
    points = np.linspace(min_x, max_x, points_number)
    return density_counting_base(numbers_for_density, points, smoothing_function, percent_sigma)


def get_logariphmated_graph_x(data):
    return [(np.log(s1), s2) for s1, s2 in data if s1 != 0]

def get_exponentated_graph_x(data):   # exponentated
    return [(np.exp(s1), s2) for s1, s2 in data]


def exponentate_graph_x(data):
    for i in range(len(data)):
        data[i] = (np.exp(data[i][0]), data[i][1])


def logariphmate_graph_x(data):
    for i in range(len(data)):
        data[i] = (np.log(data[i][0]) if data[i][0] != 0 else -100, data[i][1])

def smooth_graph_as_exp(data : list, percent_sigma : float = 0.5, point_number : float = None):
    exped = get_exponentated_graph_x(data)
    return get_logariphmated_graph_x(smooth_graph(exped, percent_sigma, combi_smoothing, point_number))


def smooth_graph_as_log(data : list, percent_sigma : float = 0.5, point_number : float = None):
    logged = get_logariphmated_graph_x(data)            # name is too long
    return get_exponentated_graph_x(smooth_graph(logged, percent_sigma, combi_smoothing, point_number))

"""
def plot_tuple_graph(data : list):
    data_xs = []
    data_ys = []
    for x, y in data:
        data_xs.append(x)
        data_ys.append(y)
    plt.plot(data_xs, data_ys)
"""

"""
def print_as_json(data : object):
    j = json.s(data)
    print(json.dumps(j, indent=4))
"""

def test_smoothing():
    """
    testing_smoothing : Final = [
        (0, 1),
        (2, 0),
        (50, 1),
        (100, 7)
    ]               
    """

    # testing_smoothing : Final = [
    #     [ 0. , 157.31799316],
    #     [ 2113. , 183.59713745],
    #     [ 4226. , 152.10749817],
    #     [ 6339. , 165.4584198 ],
    #     [ 8452. , 148.52165222],
    #     [10565. , 195.10722351],
    #     [12678. , 184.02459717],
    #     [14791. , 154.00990295],
    #     [16904. , 153.58700562],
    #     [19017. , 181.10574341]
    # ]

    testing_graph = [
        (1, 1),
        (1.5, 1.1),
        (2, 2),
        (3, 0.1),
        (4, 3.1),
    ]

    combi_smoothed = smooth_graph(testing_graph, 0.1, combi_smoothing, 1000)
    normal_smoothed = smooth_graph(testing_graph, 0.1, smoothing_normal, 1000)

    plt.plot([i[0] for i in testing_graph], [i[1] for i in testing_graph], label = "Initial points")
    plt.plot([i[0] for i in combi_smoothed], [i[1] for i in combi_smoothed], label = "Combi smoothed")
    plt.plot([i[0] for i in normal_smoothed], [i[1] for i in normal_smoothed], label = "Normal smoothed")

    plt.legend()
    plt.show()


def test_density_counting():
    numbers = [
        1,
        1.1,
        3,
        2,
        2.2,
        2.1,
        1.9,
        1.5,
        2.5,
        2.9,
        5
    ]

    res = count_density(numbers, 0.07, 100, smoothing_normal)

    plt.plot([i[0] for i in res], [i[1] for i in res])
    plt.scatter(numbers, [0] * len(numbers))
    plt.show()




def count_graph_area(graphic : list) -> float:
    accum = 0
    last : tuple
    for index, point in enumerate(graphic):
        dx = 0 if index == 0 else point[0] - last[0]
        accum += (dx * (point[1] + last[1]) / 2) if index != 0 else (dx * point[1])
        last = point
    return accum

if __name__ == "__main__":
    test_smoothing()
    # test_density_counting()
