import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def split_list_an_empty_line(list_string):
    list_string = [i.replace("\n", "") for i in list_string]
    index = list_string.index("")
    return list_string[:index], list_string[index+1:]


def split_list_by_string_an_comma(list_string):
    pattern = r'(\d+)'
    new_list_parameters = []
    for string in list_string:
        number_txt_list = re.findall(pattern, string)
        number_list = [int(i) for i in number_txt_list]
        new_list_parameters.append(number_list)
    return new_list_parameters
    # new_list_parameters = []
    # for string in list_string:
    #     list_parameter = string.replace("}", "").replace("{", "").split(",")
    #     new_list_parameters.append(list_parameter)
    # return new_list_parameters


def parser_work_processes_in_dict(list_string):
    new_dict = {}
    for string in list_string:
        list_part_of_line = string.replace("}", "").split("{")
        two_list_part_of_line = list_part_of_line[1].split(",")
        list_value = []
        for i in two_list_part_of_line:
            fri_list_part_of_line = i.split(":")
            if len(fri_list_part_of_line) == 2:
                list_value.append([fri_list_part_of_line[0],fri_list_part_of_line[1]])
            else:
                list_value.append(["True", fri_list_part_of_line[0]])
        new_dict.update({list_part_of_line[0]:list_value})
    return new_dict


def apply_instructions(dict_instructions, key, detail):

    x, m, a, s = detail
    for condition, process in dict_instructions[key]:
        if eval(condition):
            return process


def distribute_detail(detail, dict_instructions):
    key = "in"
    while key not in ["A","R"]:
        key = apply_instructions(dict_instructions, key, detail)
    return key


def distribute_all_details(list_detail, dict_instructions):
    list_detail_a = []
    list_detail_r = []
    for one_detail in list_detail:
        type_detail = distribute_detail(one_detail, dict_instructions)
        if type_detail == "A":
            list_detail_a.append(one_detail)
        elif type_detail == "R":
            list_detail_r.append(one_detail)
    return list_detail_a, list_detail_r


t1 = time.time()
work_processes_str, details = split_list_an_empty_line(list_txt)
details = split_list_by_string_an_comma(details)
work_processes = parser_work_processes_in_dict(work_processes_str)
list_a_detail, list_r_detail = distribute_all_details(details, work_processes)
sum_params_details = sum([sum(i) for i in list_a_detail])
t2 = time.time()
print(f"Решение задания 1: {sum_params_details}")
print(f"время {t2-t1}")


def find_boundary_of_range(text):
    pattern = f'(\\d+)'
    number = re.search(pattern, text).group()
    return int(number)


def calculate_options(diapason):
    options = 1
    for key, value in diapason.items():
        options = options * (value[1] - value[0] - 1)
    return options


def calculate_distribution_possibilities(diapason_original, list_key,dict_manual):
    diapason = copy.deepcopy(diapason_original)
    sum_options_ful = 0
    for rule in dict_manual[list_key[-1]]:

        if rule[0] != 'True':
            diapason_double = copy.deepcopy(diapason)
            value = find_boundary_of_range(rule[0])
            if rule[0][1] == ">":
                diapason_double[rule[0][0]][0] = max(diapason_double[rule[0][0]][0], value)
                diapason[rule[0][0]][1] = min(diapason_double[rule[0][0]][1], value+1)
            if rule[0][1] == "<":
                diapason_double[rule[0][0]][1] = min(diapason_double[rule[0][0]][1], value)
                diapason[rule[0][0]][0] = max(diapason_double[rule[0][0]][0], value - 1)
        else:
            diapason_double = diapason
        if rule[1] == "R":
            # return 0
            continue
        elif rule[1] in list_key:
            continue
            # print(f"Плохой путь {list_key} -> {rule[1]}")
            # return 0
        elif rule[1] !="A":
            new_list_key = copy.deepcopy(list_key)
            new_list_key.append(rule[1])
            sum_options_ful += calculate_distribution_possibilities(diapason_double, new_list_key,dict_manual)
        elif rule[1] == "A":
            print(list_key)
            # print(calculate_options(diapason_double))
            sum_options_ful += calculate_options(diapason_double)
        else:
            print(f"Что то не так  {list_key} -> {rule[1]}")

    return sum_options_ful

t1 = time.time()
diapason_max = {"x": [0, 4001], "m": [0, 4001], "a": [0, 4001], "s": [0, 4001]}
sum_options = calculate_distribution_possibilities(diapason_max,["in"],work_processes)
t2 = time.time()
print(f"Решение задания 2: {sum_options}")
print(f"время {t2-t1}")