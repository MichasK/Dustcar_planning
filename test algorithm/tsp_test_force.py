from data_structers.individual import Individual, Population
from data_structers.inputdata import InputData
from data_structers.evolutional_algorithm import evolution_simulator
import random
from datetime import datetime
import copy
import numpy as np
from import_data.distance_matrix_calculator import matrix_array_calculate
import os

random.seed(datetime.now())

data_set = 'trivial'

gmina = "../data/" + data_set

csv_output = "../Reports/" + 'tsp_' + data_set + ".csv"
order_outpur = "../Reports/" + 'tsp_' + data_set + ".txt"
best_solution = 1000000
matrix_array_calculate(gmina + "_streets.csv", gmina + "_distance_matrix")
inp_data = InputData(gmina)

x = Individual(inp_data)
for i in range(100000):
    x.street_order = np.arange(1, 7)
    np.random.shuffle(x.street_order)
    x.calculate_cost_value(inp_data)
    if x.cost_function_value < best_solution:
        best_solution = x.cost_function_value

print(best_solution)
