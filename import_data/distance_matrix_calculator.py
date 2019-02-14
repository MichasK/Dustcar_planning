import numpy as np
import pandas as pd
from geopy import distance


def matrix_array_calculate(src: str, dst: str) -> None:
    data = pd.read_csv(src, header=0)
    long = data.longitude
    lat = data.latitude

    size = long.count()
    distances = np.zeros([size, size])

    for i in range(0, size):
        for j in range(0, size):
            p1 = (long[i], lat[i])
            p2 = (long[j], lat[j])
            val = round(distance.distance(p1, p2).km,3)
            distances[i][j] = val

    # print(distances)

    np.savetxt(dst+".csv", distances, delimiter=",")
    np.save(dst+".npy",distances)


matrix_array_calculate("../data/parsed.csv", "../data/distance_matrix")

