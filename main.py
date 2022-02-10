""""my lab"""
import argparse
import doctest
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import folium

PARSER = argparse.ArgumentParser(description="search and replaces the specified element")
PARSER.add_argument("year", type=str, help="")
PARSER.add_argument("latitude", type=float, help="latitude of ur location")
PARSER.add_argument("longitude", type=float, help="longitude of ur location")
PARSER.add_argument("path", type=str, help="path to dataset")
ARGS = PARSER.parse_args()
YEAR = ARGS.year
LAT = ARGS.latitude
LON = ARGS.longitude
PATH = ARGS.path

def distance(lat1, lat2, lon1, lon2):
    """
    Function returns a distance between two points
    which are given in latitude and longitude format
    >>> distance(49.83826, 48.287312, 24.02324, 25.1738)
    191.74583209959988
    """
    radius = 6371
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    first_part = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    second_part = 2 * asin(sqrt(first_part))
    res = second_part * radius
    return res


def main(year: str, lat: float, lon: float, path: str):
    """
    The main function works with year of move, latitude, longtitude of ur place
    and path to the dataset. Function main returns a list wich consist of
    name of move, dictance to ur point, lat, lon2
    """
    res_list = []
    counter = 0
    with open(path, "r", encoding="utf-8", errors='ignore') as file:
        for line in file:
            if line == "==============\n":
                counter += 1
            if counter != 0:
                if year in line:
                    new_line = line[:-1].replace("(", "|").replace(")", "|").replace("}", "")
                    if new_line[-1] == '|':
                        new_line = new_line.split("|")
                        if new_line[1] == year:
                            name = new_line[0].replace("'", "")
                            place = new_line[-3].replace("\t", "")
                            # print(name)
                            try:
                                geolocator = Nominatim(user_agent="olehh")
                                location = geolocator.geocode(place)
                                lat2 = location.latitude
                                lon2 = location.longitude
                                dictance = distance(lat, lat2, lon, lon2)
                                if (name[1:-2], dictance, lat2, lon2) not in res_list:
                                    res_list.append((name[1:-2], dictance, lat2, lon2))
                            except AttributeError:
                                pass
                    else:
                        new_line = new_line.split("|")
                        if new_line[1] == year:
                            name = new_line[0].replace("'", "")
                            place = new_line[-1].replace("\t", "")
                            try:
                                geolocator = Nominatim(user_agent="olehh")
                                location = geolocator.geocode(place)
                                lat2 = location.latitude
                                lon2 = location.longitude
                                dictance = distance(lat, lat2, lon, lon2)
                                if (name[1:-2], dictance, lat2, lon2) not in res_list:
                                    res_list.append((name[1:-2], dictance, lat2, lon2))
                            except AttributeError:
                                pass
    sorted_list = sorted(res_list, key=lambda kv: kv[1])
    return sorted_list


def map_making(lat, lon, list_of_moves):
    """
    The function makes an HTML file of 10 points in the world map
    and names
    """
    my_map = folium.Map(tiles="Stamen Terrain",\
    location=[lat, lon], zoom_start=10)
    stp = folium.FeatureGroup(name="Star point")
    stp.add_child(folium.Marker(location=[lat, lon],\
    popup="your start point",\
    icon=folium.Icon(color='red', icon='home', prefix='fa')))
    film_map = folium.FeatureGroup(name="Film map")
    for i in range(10):
        film_map.add_child(folium.Marker(location=[list_of_moves[i][-2], \
            list_of_moves[i][-1]],\
            popup=list_of_moves[i][0],\
            icon=folium.Icon()))
    my_map.add_child(stp)
    my_map.add_child(film_map)
    my_map.add_child(folium.LayerControl())
    my_map.save('oleh_op.html')


LIST_OF_TUPLES = main(YEAR, LAT, LON, PATH)
try:
    map_making(LAT, LON, LIST_OF_TUPLES)
except IndexError:
    print("i'm not allowed to show less than 10 points")


if __name__ == "__main__":
    print(doctest.testmod())
# python3 main.py 2000 49.83826 24.02324 /mnt/d/labs/lab2s/locations1.list
