import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    list_element = list(str_element_map)
    return [i if i != "." else "" for i in list_element]


def add_empty_line(list_list_element, repetitions = 1):
    new_list_list_element = copy.deepcopy(list_list_element)
    dict_empty_line = {index: value for index, value in enumerate(list_list_element) if not any(value)}
    already_inserted = 0
    for key, value in dict_empty_line.items():
        new_list_list_element = (new_list_list_element[:key + already_inserted] + [value for i in range(repetitions)] +
                                 new_list_list_element[key + already_inserted:])
        # new_list_list_element.insert(key + already_inserted, value)
        already_inserted += repetitions
    return new_list_list_element


def get_indexes_empty_rows(list_list_element):
    list_index = [index for index, value in enumerate(list_list_element) if not any(value)]
    return list_index


def matrix_transposition(old_matrix):
    new_matrix = [[0 for j in range(len(old_matrix))]for i in range(len(old_matrix[0]))]
    for i in range(len(old_matrix)):
        for j in range(len(old_matrix[i])):
            new_matrix[j][i] = old_matrix[i][j]
    return new_matrix


def find_coordinates_stars(galaxy, ):
    dict_coordinates_stars = {}
    numer_stars = 0
    for i in range(len(galaxy)):
        for j in range(len(galaxy[i])):
            if galaxy[i][j]:
                dict_coordinates_stars.update({numer_stars:(i,j)})
                numer_stars +=1
    return dict_coordinates_stars


def find_distance_from_star(dict_stars,numer_stars):
    list_distance = []
    for key, value in dict_stars.items():
        if key > numer_stars:
            list_distance.append(abs(value[0] - dict_stars[numer_stars][0]) +
                                 abs(value[1] - dict_stars[numer_stars][1]))
    return {numer_stars: list_distance}


def find_full_distance_from_star(dict_stars):
    full_distance = {}
    for key in dict_stars:
        full_distance.update(find_distance_from_star(dict_stars, key))
    return full_distance


def find_full_distance_from_star_with_passion(dict_stars, list_empty_rows, list_empty_columns, hobby):
    full_distance = {}
    for key in dict_stars:
        full_distance.update(find_distance_from_star_with_passion(dict_stars, key, list_empty_rows, list_empty_columns, hobby))
    return full_distance


def find_distance_from_star_with_passion(dict_stars,numer_stars, list_empty_rows, list_empty_columns, hobby):
    list_distance = []
    for key, value in dict_stars.items():
        if key > numer_stars:
            list_hobby_rows = [i for i in list_empty_rows if dict_stars[numer_stars][0] < i < value[0]
                               or value[0] < i < dict_stars[numer_stars][0]]
            list_hobby_columns = [i for i in list_empty_columns if dict_stars[numer_stars][1] < i < value[1]
                                  or value[1] < i < dict_stars[numer_stars][1]]
            list_distance.append(abs(value[0] - dict_stars[numer_stars][0]) + hobby * len(list_hobby_rows) +
                                 abs(value[1] - dict_stars[numer_stars][1]) + hobby * len(list_hobby_columns))
    return {numer_stars: list_distance}


def find_dict_distance(dict_distance):
    summ_value = 0
    for key, values in  dict_distance.items():
        summ_value += sum(values)
    return summ_value


t1 = time.time()
start_map_galaxy = [parser_map(i) for i in list_txt]
increased_in_length_map_galaxy = add_empty_line(start_map_galaxy)
rotated_galaxy = matrix_transposition(increased_in_length_map_galaxy)
increased_rotated_galaxy = add_empty_line(rotated_galaxy)
increased_galaxy = matrix_transposition(increased_rotated_galaxy)
coordinates_ful_stars = find_coordinates_stars(increased_galaxy)
dict_distance_stars = find_full_distance_from_star(coordinates_ful_stars)
sum_distance = find_dict_distance(dict_distance_stars)
t2 = time.time()
print(f"Решение задания 1: {sum_distance}")
print(f"время {t2-t1}")




t1 = time.time()
indexes_empty_rows = get_indexes_empty_rows(start_map_galaxy)
rotated_galaxy = matrix_transposition(start_map_galaxy)
indexes_empty_columns = get_indexes_empty_rows(rotated_galaxy)

coordinates_ful_stars_2 = find_coordinates_stars(start_map_galaxy)

# find_distance_from_star_with_passion(coordinates_ful_stars_2,1, indexes_empty_rows, indexes_empty_columns, 10)
# find_distance_from_star(coordinates_ful_stars,1)

dict_distance_stars_2 = find_full_distance_from_star_with_passion(coordinates_ful_stars_2, indexes_empty_rows,
                                                                  indexes_empty_columns, 1000000 -1)
sum_distance = find_dict_distance(dict_distance_stars_2)
t2 = time.time()
print(f"Решение задания 2: {sum_distance}")
print(f"время {t2-t1}")
