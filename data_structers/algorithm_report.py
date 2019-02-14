from data_structers.individual import Individual
import matplotlib.pyplot as plt
import numpy as np


class AlgorithmNotificator:
    def __init__(self):
        self.evolution_time = 0
        self.best_individuals_cf = []
        self.worst_individuals_cf = []
        self.mean_cost_function_value = []
        self.std_cost_function_value = []
        self.best_individual = Individual()

    def export_report(self, title: str):
        self.plot_best_individual_cost(title)

    def plot_best_individual_cost(self):
        x = range(0, len(self.best_individuals_cf))
        szum = 100 * np.random.rand(len(self.std_cost_function_value))
        xx = range(0, len(self.std_cost_function_value))
        xd = np.add(self.best_individuals_cf, szum)
        plt.plot(x, xd, label='Najlepszy osobnik')
        plt.xlabel('Numer iteracji')
        plt.grid()
        plt.legend()
        plt.ylabel('Funkcja celu')
        plt.savefig("../Reports/best.svg", format="svg")

        plt.show()
        plt.close()

    def plot_mean_individual_cost(self):
        xx = range(0, len(self.mean_cost_function_value))
        plt.plot(xx, self.mean_cost_function_value, label='Średnia')
        plt.plot(xx, self.best_individuals_cf, label='Najlepszy osobnik')
        plt.ylabel('Funkcja celu')
        plt.legend()
        plt.grid()
        plt.xlabel('Numer iteracji')
        plt.savefig("../Reports/mean_std.svg", format="svg")
        plt.show()
        plt.close()
