from data_structers.individual import Individual, Population
from data_structers.inputdata import InputData
from data_structers.evolutional_algorithm import evolution_simulator
import random
from datetime import datetime
import copy
import numpy as np
from import_data.distance_matrix_calculator import matrix_array_calculate
import os

'''
Wybierz zbiór testujący, reszta plików utworzy sie na podstawie jego nazwy

'''
random.seed(datetime.now())

data_set = 'trivial'

gmina = "../data/" + data_set

csv_output = "../Reports/" + 'tsp_' + data_set + ".csv"
order_outpur = "../Reports/" + 'tsp_' + data_set + ".txt"

'''
Przygotowanie pierwszej populacji
'''

# find_cords(gmina+"_streets.csv", gmina+"_streets.csv")
matrix_array_calculate(gmina + "_streets.csv", gmina + "_distance_matrix")
inp_data = InputData(gmina)
'''

Przygotowanie plików autput

'''
if os.path.exists(csv_output):
    os.remove(csv_output)
if os.path.exists(order_outpur):
    os.remove(order_outpur)
os.mknod(csv_output)
with open(csv_output, 'a') as fd:
    fd.write('Populacja,Liczba iteracji,P(krzyżowanie),P(mutacja),Rozmiar Turnieju,Krzyżowanie losowe,Krzyżowanie podciąg,Usuń samochód,Przesuń samochód,Dodaj powrót,Usuń powrót,Dodaj samochód,Zamień węzły,Zamień składowe,Funkcja celu')
    fd.write('\n')
for i in range(1, 15):

    population = random.randint(10, 30)
    first_pop = Population()
    for i in range(population):
        x = Individual(inp_data)
        x.calculate_cost_value(inp_data)
        first_pop.append(x)

    '''
    
    Ustawienie nastaw  instancji
    
    '''
    MAX_ITERATIONS = random.randint(5, 20)
    cross_propability = random.randint(1, 15)
    mutation_propability = random.randint(1, 15)
    tournament_size = random.randint(2, 15)
    configuration_parameters = str(population) + ',' + str(MAX_ITERATIONS) + ',' + str(cross_propability) + ',' + str(
        mutation_propability) + ',' + str(tournament_size) + ','
    population_history = copy.deepcopy(
        evolution_simulator(initial_population=first_pop, max_iteration=MAX_ITERATIONS, inp_data=inp_data,
                            cross_coe=cross_propability,
                            mutation_coe=mutation_propability, turnament_size=tournament_size))

    ''''
    
    Eksport wynikow
    
    '''
    population_history.best_individual.show_indyvidual(inp_data)

    print(population_history.best_individual.street_order)
    print(population_history.best_individual.cost_function_value)

    population_history.plot_best_individual_cost()
    population_history.plot_mean_individual_cost()

    new_row = configuration_parameters + str(population_history.best_individual.genesis) + ',' + str(
        population_history.best_individual.cost_function_value) + '\n'
    re_array = np.concatenate((np.array([-1, 0]), population_history.best_individual.street_order, np.array([0])),
                              axis=None)
    output_vec = str(re_array) + '\n'
    with open(csv_output, 'a') as fd:
        fd.columns = ['population', 'MAX_ITERATIONS', 'cross_propability', 'mutation_propability', 'tournament_size',
                      'cross_indvidual_random_counter', 'cross_indvidual_longest_common_counter',
                      'delete_random_car_counter', 'shift_car_counter', 'add_random_comeback_counter',
                      'delete_random_comeback_counter',
                      'add_random_car_counter', 'swap_element_order_counter', 'change_random_element_counter',
                      'cost_function']
        fd.write(new_row)
        print('dupaa')

    with open(order_outpur, 'a') as fd:
        fd.write(output_vec)
