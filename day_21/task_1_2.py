import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    return list(str_element_map)


def find_coordinates_s(list_map_line):
    for index_map_line in range(len(list_map_line)):
        for index_point_map in range(len(list_map_line[index_map_line])):
            if list_map_line[index_map_line][index_point_map] == "S":
                return index_map_line, index_point_map, 0, 0


def check_validity(new_coordinates,ful_map):
    if new_coordinates[0] < 0:
        new_coordinates[2] -= 1
        new_coordinates[0] = len(ful_map) + new_coordinates[0]
    if new_coordinates[0] >= len(ful_map):
        new_coordinates[2] += 1
        new_coordinates[0] = new_coordinates[0] - len(ful_map)
    if new_coordinates[1] < 0:
        new_coordinates[3] -= 1
        new_coordinates[1] = len(ful_map[0]) + new_coordinates[1]
    if new_coordinates[1] >= len(ful_map[0]):
        new_coordinates[3] += 1
        new_coordinates[1] = new_coordinates[1] - len(ful_map[0])
    if ful_map[new_coordinates[0]][new_coordinates[1]] == "#":
        return None
    else:
        return new_coordinates


def find_possible_steps(coordinates_start, ful_map):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    list_new_coordinates = []
    for option in directions:
        new_coordinates = [coordinates_start[0]+option[0], coordinates_start[1]+option[1],
                           coordinates_start[2], coordinates_start[3]]
        new_coordinates = check_validity(new_coordinates, ful_map)
        if new_coordinates:
            list_new_coordinates.append(tuple(new_coordinates))
        # if new_coordinates[0] < 0:
        #     new_coordinates[2] -= 1
        #     new_coordinates[0] = len(ful_map) + new_coordinates[0]
        # if new_coordinates[0] >= len(ful_map):
        #     new_coordinates[2] += 1
        #     new_coordinates[0] = new_coordinates[0]-len(ful_map)
        # if new_coordinates[1] < 0:
        #     new_coordinates[3] -= 1
        #     new_coordinates[1] = len(ful_map[0]) + new_coordinates[1]
        # if new_coordinates[1] >= len(ful_map[0]):
        #     new_coordinates[3] += 1
        #     new_coordinates[1] = new_coordinates[1] - len(ful_map[0])
        # if ful_map[new_coordinates[0]][new_coordinates[1]] == "#":
        #     continue
        # else:
        #     list_new_coordinates.append(tuple(new_coordinates))
    return list_new_coordinates


def take_few_steps(count_steps, ful_map, coordinates_start):
    list_coordinates = set([coordinates_start])
    for index_steps in range(count_steps):
        new_list_coordinates = set()
        for start_option in list_coordinates:
            list_coordinates_option = find_possible_steps(start_option, ful_map)
            new_list_coordinates = new_list_coordinates.union(list_coordinates_option)
            # print()
        # print(f"Шаг иджекс {index_steps}")
        # print(new_list_coordinates)
        list_coordinates = new_list_coordinates
        # print(len(list_coordinates))
    return list_coordinates


def calculate_number_of_fields_after_several_steps(count_steps, ful_map, coordinates_start):
    actual_set_coordinates = {coordinates_start}
    old_set_coordinates = set()
    sum_field = [0, 1]
    index_sum = 0
    for index_steps in range(count_steps):
        new_set_coordinates = set()
        for start_option in actual_set_coordinates:
            list_coordinates_option = find_possible_steps(start_option, ful_map)
            new_set_coordinates = new_set_coordinates.union(list_coordinates_option)
        new_set_coordinates = new_set_coordinates - old_set_coordinates
        # new_set_coordinates = (
        #     new_set_coordinates.union([find_possible_steps(start_option, ful_map)
        #                                for start_option in actual_set_coordinates]) - old_set_coordinates)
        old_set_coordinates = actual_set_coordinates
        actual_set_coordinates = new_set_coordinates
        index_sum = index_steps % 2
        sum_field[index_sum] += len(actual_set_coordinates)
    return sum_field[index_sum]


t1 = time.time()
start_map_galaxy = [parser_map(i) for i in list_txt]
# [print(i) for i in start_map_galaxy]
start_point = find_coordinates_s(start_map_galaxy)
# print(start_point)
finish_coordinates = take_few_steps(64,start_map_galaxy,start_point)
answer = len(finish_coordinates)
t2 = time.time()
print(f"Решение задания 1: {answer}")
print(f"время {t2-t1}")


def big_calculate_number_of_fields_after_several_steps(count_steps, ful_map, coordinates_start):
    old_sum = 0
    old_difference = 0
    old_difference_difference = 0
    start_count_steps = count_steps % len(ful_map)
    steps = start_count_steps
    step_length = len(ful_map)
    while steps <= count_steps:
        global_sum = calculate_number_of_fields_after_several_steps(steps, ful_map, coordinates_start)
        difference = global_sum - old_sum
        difference_difference = difference - old_difference
        if old_difference_difference == difference_difference and steps:
            n = int((count_steps - steps) / step_length)
            big_difference = (n*(n+1))/2 * difference_difference + difference *n
            return global_sum + big_difference
        old_difference_difference = difference - old_difference
        old_sum = global_sum
        old_difference = difference
        steps += step_length


t1 = time.time()
start_map_galaxy = [parser_map(i) for i in list_txt]
start_point = find_coordinates_s(start_map_galaxy)
ful_count_steps = 26501365
answer = big_calculate_number_of_fields_after_several_steps(ful_count_steps, start_map_galaxy, start_point)
t2 = time.time()
print(f"Решение задания 2: {answer}")
print(f"время {t2-t1}")