import copy
import re
import collections
import time
import math

with open("input_stas.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    matches = re.findall(r"(-?\d+)", str_element_map)
    return tuple(int(i) for i in matches)


def parser_reverse_map(str_element_map):
    matches = re.findall(r"(-?\d+)", str_element_map)
    matches.reverse()
    return tuple(int(i) for i in matches)


def find_list_of_differences(list_values):
    list_of_differences = []
    for i in range(1, len(list_values)):
        list_of_differences.append(list_values[i]-list_values[i-1])
    return tuple(list_of_differences)


def find_list_of_lists_of_differences(list_values,exit_condition):
    list_of_lists_of_differences = [list_values]
    while not exit_condition(list_of_lists_of_differences[-1]):
        list_of_differences = find_list_of_differences(list_of_lists_of_differences[-1])
        list_of_lists_of_differences.append(list_of_differences)
    return list_of_lists_of_differences


return_condition = lambda x: len(set(x))==1
# return_condition = lambda x: all([i==0 for i in x])

t1 = time.time()
list_original_sequence = tuple(parser_map(i) for i in list_txt)

list_of_lists_sequence = [find_list_of_lists_of_differences(i, return_condition) for i in list_original_sequence]

list_next_sequence = [sum([j[-1] for j in i]) for i in list_of_lists_sequence]

t2 = time.time()
print(f"Решение задания 1: {sum(list_next_sequence)}")
print(f"время {t2-t1}")

t1 = time.time()

list_original_sequence = tuple(parser_reverse_map(i) for i in list_txt)

list_of_lists_sequence = [find_list_of_lists_of_differences(i, return_condition) for i in list_original_sequence]

list_next_sequence = [sum([j[-1] for j in i]) for i in list_of_lists_sequence]

t2 = time.time()
print(f"Решение задания 2: {sum(list_next_sequence)}")
print(f"время {t2-t1}")