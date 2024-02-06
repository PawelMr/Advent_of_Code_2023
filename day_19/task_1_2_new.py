import copy
import re
import collections
import time
import math

with open("test.txt", mode="r", encoding="utf-8") as test_file:
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


def get_key_instruction(string):
    key, rest_of_line = string.split("{")
    return key


def find_next_line(purpose, list_instructions_str):
    for string in list_instructions_str:
        if ":"+purpose+"," in string or ","+purpose+"}" in string:
            if string.index(purpose):
                return string


def make_map(string,list_instructions_str):
    key = get_key_instruction(string)
    list_transitions = [key]
    while key != "in":
        new_string = find_next_line(key, list_instructions_str)
        key = get_key_instruction(new_string)
        if key in list_transitions:
            return None
        list_transitions.append(key)
    list_transitions.reverse()
    return list_transitions


def get_list_map(list_instructions_str):
    list_maps = []
    for string in list_instructions_str:
        if "A" in string:
            list_maps.append(make_map(string,list_instructions_str))
    return list_maps


def find_boundary_of_range(text):
    pattern = f'(\\d+)'
    number = re.search(pattern, text).group()
    return int(number)


def shorten_range(condition,next_key, diapason):
    for condition in condition:
        if condition[1] != next_key:
            if condition[0][1] == "<":
                value_rule = find_boundary_of_range(condition[0])
                diapason[condition[0][0]][0] = max(diapason[condition[0][0]][0], value_rule-1)
            if condition[0][1] == ">":
                value_rule = find_boundary_of_range(condition[0])
                diapason[condition[0][0]][1]= min(diapason[condition[0][0]][1], value_rule+1)
        if condition[1] == next_key:
            if condition[0][1] == ">":
                value_rule = find_boundary_of_range(condition[0])
                diapason[condition[0][0]][0] = max(diapason[condition[0][0]][0], value_rule)
            if condition[0][1] == "<":
                value_rule = find_boundary_of_range(condition[0])
                diapason[condition[0][0]][1] = min(diapason[condition[0][0]][1], value_rule)
            return diapason


def calculate_options(diapason):
    options = 1
    for key, value in diapason.items():
        options = options * (value[1] - value[0] - 1)
    return options


def swipe_range_on_map(maps, dict_instructions):
    diapason = {"x": [0, 4001], "m": [0, 4001], "a": [0, 4001], "s": [0, 4001]}
    for step in range(len(maps) - 1):
        condition = dict_instructions[maps[step]]
        next_key = maps[step+1]
        diapason = shorten_range(condition,next_key, diapason)
    number_out = [i for i,j in enumerate(dict_instructions[maps[-1]]) if j[1] == "A"]
    if len(number_out)>1:
        return check_many_outputs(number_out, diapason, dict_instructions[maps[-1]])
    else:
        diapason = shorten_range(dict_instructions[maps[-1]], "A", diapason)
        print(diapason)
        return calculate_options(diapason), [diapason]


def check_many_outputs(number_out,diapason, instruction):
    # print(instruction)
    list_double_diapason = []
    list_options = []
    revers_number_out = copy.deepcopy(number_out)
    revers_number_out.reverse()
    print("___________________")
    for i in number_out:
        double_diapason = copy.deepcopy(diapason)
        double_condition = copy.deepcopy(instruction)

        for j in revers_number_out:
            if i != j:
                double_condition.pop(j)
        double_diapason = shorten_range(double_condition, "A", double_diapason)
        print("или")
        print(double_diapason)
        list_double_diapason.append(double_diapason)
        list_options.append(calculate_options(double_diapason))
    print("___________________")
    return max(list_options), list_double_diapason


def get_list_positive_instruction_txt(list_instructions_str):
    new_list_positive_instruction_txt = [i for i in list_instructions_str if "A" in i]
    return new_list_positive_instruction_txt


def get_all_follow_chain_of_rules(list_positive_instruction_txt, dict_instructions):
    sum_options_instruction = 0
    ful_list_diapason = []
    for instruction_txt in list_positive_instruction_txt:
        options_instruction, list_diapason = swipe_range_on_map(instruction_txt, dict_instructions)
        sum_options_instruction += options_instruction
        ful_list_diapason.extend(list_diapason)
        # print(options_instruction)
    return sum_options_instruction, ful_list_diapason


def find_incoming_ranges(ful_list_diapason):
    new_ful_list_diapason = []
    for diapason in ful_list_diapason:
        flag_set = True
        for index, passed_diapason in enumerate(new_ful_list_diapason):
            if (passed_diapason["x"][0]<=diapason["x"][0] and passed_diapason["x"][1]>=diapason["x"][1] and
                    passed_diapason["m"][0]<=diapason["m"][0] and passed_diapason["m"][1]>=diapason["m"][1]and
                    passed_diapason["a"][0]<=diapason["a"][0] and passed_diapason["a"][1]>=diapason["a"][1]and
                    passed_diapason["s"][0]<=diapason["s"][0] and passed_diapason["s"][1]>=diapason["s"][1]):
                flag_set = False
            if (passed_diapason["x"][0] >= diapason["x"][0] and passed_diapason["x"][1] <= diapason["x"][1] and
                    passed_diapason["m"][0] >= diapason["m"][0] and passed_diapason["m"][1] <= diapason["m"][1] and
                    passed_diapason["a"][0] >= diapason["a"][0] and passed_diapason["a"][1] <= diapason["a"][1] and
                    passed_diapason["s"][0] >= diapason["s"][0] and passed_diapason["s"][1] <= diapason["s"][1]):
                new_ful_list_diapason[index]= diapason
                flag_set = False
                break
        if flag_set:
            new_ful_list_diapason.append(diapason)
    return new_ful_list_diapason


# Неверно считает на больших данных а на тестовых верно
t1 = time.time()
list_maps_instructions = get_list_map(work_processes_str)
sum_options, ful_diapason = get_all_follow_chain_of_rules(list_maps_instructions, work_processes)
new_ful_diapason = find_incoming_ranges(ful_diapason)
list_options = [calculate_options(i) for i in new_ful_diapason]
t2 = time.time()
print(f"Решение задания 2: {sum_options}")
print(f"Решение задания 2: {sum(list_options)}")
print(f"время {t2-t1}")