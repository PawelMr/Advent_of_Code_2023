import copy
import re
import collections
import time
import math
from itertools import *

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


def get_index_substitutions_list(string):
    pattern = r"\?"
    matches = list(re.finditer(pattern, string))
    substitutions_list = [i.start() for i in matches]
    return substitutions_list


def add_index_substitutions_list(list_element):
    for element in list_element:
        substitutions_list = get_index_substitutions_list(element[0])
        element.append(substitutions_list)


def split_string(list_str):
    list_list_str = []
    for str in list_str:
        element = str.split(' ')
        element[1] = disassemble_into_numbers(element[1])
        list_list_str.append(element)
    return list_list_str


def get_list_possible_substitutions(list_element):
    new_list_possible_substitutions = []
    for i in list_element:
        new_list_possible_substitutions.append(list(product('#.', repeat=len(i[2]))))
    return new_list_possible_substitutions


def remove_unnecessary_substitutions(list_element, list_substitutions):
    new_short_list_substitutions = []
    for i in range(len(list_element)):
        new_short_list_substitutions.append([])
        for j in range(len(list_substitutions[i])):
            s = bytearray(list_element[i][0], 'utf-8')
            for z in range(len(list_element[i][2])):
                s[list_element[i][2][z]] = bytes(list_substitutions[i][j][z], 'utf-8')[0]
            string = str(s, 'utf-8')
            if disassemble_into_grid(string) == list_element[i][1]:
                new_short_list_substitutions[i].append(list_substitutions[i][j])
    return new_short_list_substitutions


def disassemble_into_grid(string):
    pattern = r'(#+)'
    matches = list(re.finditer(pattern, string))
    list_interval = [len(i.group(1)) for i in matches]
    return list_interval


# def split_springs(string):
#     list_springs = string.split('.')
#     list_springs = [i for i in list_springs if i]
#     return list_springs
#
#
# def remove_unambiguous_elements(list_element):
#     new_list = []
#     for old_element in list_element:
#         element = copy.deepcopy(old_element)
#         for i in range(len(element[0])):
#             if i < len(element[0]) and i < len(element[1]) and len(element[0][i]) < min(element[1]):
#                 element[0].pop(i)
#
#         for i in range(-1, -1*len(element[0]) - 1, -1):
#
#             if i >= -1*len(element[0]) and i >= -1*len(element[1]) and len(element[0][i]) == element[1][i]:
#                 element[0].pop(i)
#                 element[1].pop(i)
#
#
#         for i in range(len(element[0])):
#             if i < len(element[1]) and i < len(element[0]) and len(element[0][i]) == element[1][i]:
#                 element[0].pop(i)
#                 element[1].pop(i)
#         new_list.append(element)
#     return new_list
#
#
# def remove_unambiguous_two_elements(list_element):
#     new_list = []
#     for old_element in list_element:
#         element = copy.deepcopy(old_element)
#         if len(element[0])>0:
#             list_grid = disassemble_into_grid(element[0][0])
#             if list_grid:
#                 if element[1] and len(list_grid[0].group(1)) == element[1][0]:
#                     element[0][0] = element[0][0][list_grid[0].end()+1:]
#                     element[1].pop(0)
#
#                 try:
#                     if element[1] and len(list_grid[-1].group(1)) == element[1][-1]:
#                         element[0][0] = element[0][0][:list_grid[0].start()-1]
#                         element[1].pop(-1)
#                 except Exception as e:
#                     raise AssertionError(f"")
#                 if len(element[1]) == 0:
#                     element[0] = []
#         new_list.append(element)
#     return new_list
#
#
# def count_combinations(len_list, list_section):
#     for i in list_section:
#         len_list -= i-1
#     len_list -= len(list_section)-1
#     count = math.factorial(len_list) / math.factorial(len_list - len(list_section))/math.factorial(len(list_section))
#     return int(count)
#
#
# def calculate_options(list_element):
#     list_options = []
#     for element in list_element:
#         if len(element[0]) == 0:
#             list_options.append(1)
#         if len(element[0]) == 1:
#             list_options.append(count_combinations(len(element[0][0]), element[1]))
#         if len(element[0]) > 1:
#             if len(element[0]) == len(element[1]):
#                 sum_options = 0
#                 for i in range(len(element[0])):
#                     sum_options += count_combinations(len(element[0][i]), [element[1][i]])
#                 list_options.append(sum_options)
#             else:
#                 raise Exception("Фиг знает как обработать")
#     return list_options


list_data_sheet = split_string(list_txt)
add_index_substitutions_list(list_data_sheet)
list_possible_substitutions = get_list_possible_substitutions(list_data_sheet)

short_list_substitutions = remove_unnecessary_substitutions(list_data_sheet, list_possible_substitutions)
len_short_list_substitutions = [len(i) for i in short_list_substitutions]

print(f"Решение задания 1: {sum(len_short_list_substitutions)}")


def get_new_list_data_sheet(list_element):
    new_list_element = []
    old_list_element = copy.deepcopy(list_element)
    for element in old_list_element:
        list_new_string = [element[0] for i in range(5)]
        new_string = "?".join(list_new_string)
        new_cart = element[1]*5
        new_list_element.append([new_string, new_cart])
    return new_list_element


# убивает оперативку
# new_list_data_sheet = get_new_list_data_sheet(split_string(list_txt))
# add_index_substitutions_list(new_list_data_sheet)
# list_possible_substitutions = get_list_possible_substitutions(new_list_data_sheet)
#
# short_list_substitutions = remove_unnecessary_substitutions(new_list_data_sheet, list_possible_substitutions)
# len_short_list_substitutions = [len(i) for i in short_list_substitutions]
#
# print(f"Решение задания 1: {sum(len_short_list_substitutions)}")