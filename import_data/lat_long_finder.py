import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import time


def find_cords(src: str, dst: str) -> None:
    '''

    :param src:Path to source file
    :param dst:Path to write result
    :return:
    '''
    df = pd.read_csv(src, header=0)
    long = []
    lat = []
    geolocator = Nominatim(user_agent="DustCar-planning")
    for index, row in df.iterrows():
        time.sleep(0.00001)
        place = row.powiat+" "+row.miejscowosc + " " + row.ulica + " " + row.numer
        location = geolocator.geocode(place)
        if location is None:
            long.append(0)
            lat.append(0)
            # raise RuntimeError('Location not found: ' + place)
        else:
            long.append(location.longitude)
            lat.append(location.latitude)

    df['latitude'] = lat
    df['longitude'] = long
    df.to_csv(dst,",",",",None,None,True,False)
