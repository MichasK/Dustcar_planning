import numpy as np
import pandas as pd


class InputData:

    def __init__(self, gmina: str) -> None:
        self.gmina = gmina
        self.distance_matrix = np.load(gmina + "_distance_matrix.npy")
        self.streets = pd.read_csv(gmina + "_streets.csv", header=0)
        self.streets_ilosc_koszy=np.array(self.streets.ilosc_koszy)
        self.streets_ilosc_posesji=np.array(self.streets.ilosc_posesji)
        self.cars = pd.read_csv(gmina + "_cars.csv", header=0)
        self.cars_pojemnosc=np.array(self.cars.pojemnosc)