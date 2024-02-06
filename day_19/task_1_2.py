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


def find_boundary_of_range(text):
    pattern = f'(\\d+)'
    number = re.search(pattern, text).group()
    return int(number)


def modern_diapason_by_processes(instruction, diapason, purpose):
    number_occurrences = 0
    list_new_diapason = []
    for i in instruction:
        if i[1] == purpose:
            number_occurrences +=1
    # if number_occurrences >1:
    #     print(instruction)
    for rule, value in instruction:
        if value != purpose:
            if rule[1] == "<":
                value_rule = find_boundary_of_range(rule)
                diapason[rule[0]][0] = max(diapason[rule[0]][0], value_rule-1)
            elif rule[1] == ">":
                value_rule = find_boundary_of_range(rule)
                diapason[rule[0]][1] = min(diapason[rule[0]][1], value_rule+1)
        else:
            number_occurrences -= 1
            list_new_diapason.append(copy.deepcopy(diapason))
            new_diapason = list_new_diapason[-1]
            if rule[1] == ">":
                value_rule = find_boundary_of_range(rule)
                new_diapason[rule[0]][0] = max(new_diapason[rule[0]][0], value_rule)
            elif rule[1] == "<":
                value_rule = find_boundary_of_range(rule)
                new_diapason[rule[0]][1] = min(new_diapason[rule[0]][1], value_rule)
            if number_occurrences == 0:
                break
    if len(list_new_diapason) ==1:
        diapason = list_new_diapason[0]
    else:
        return list_new_diapason
    return diapason


def get_key_instruction(string):
    key, rest_of_line = string.split("{")
    return key


def find_next_line(purpose, list_instructions_str):
    for string in list_instructions_str:
        if ":"+purpose+"," in string or ","+purpose+"}" in string:
            if string.index(purpose):
                return string


def follow_chain_of_rules(instruction_txt, dict_instructions, list_instructions_str):
    diapason = {"x": [0, 4001], "m": [0, 4001], "a": [0, 4001], "s": [0, 4001]}
    list_options = []
    string = instruction_txt
    key = get_key_instruction(string)
    diapason = modern_diapason_by_processes(dict_instructions[key], diapason, "A")
    if isinstance(diapason, dict):
        list_diapason = [diapason]
    else:
        list_diapason = diapason
    purpose_start = key
    string_start = find_next_line(purpose_start, list_instructions_str)

    for diapason in list_diapason:
        purpose = purpose_start
        string = string_start
        list_key = []
        while key != "in":
            key = get_key_instruction(string)
            if key in list_key:
                return 0
            diapason = modern_diapason_by_processes(dict_instructions[key], diapason, purpose)
            purpose = key
            string = find_next_line(purpose, list_instructions_str)
            list_key.append(key)
        options = 1
        for key, value in diapason.items():
            options = options * (value[1] - value[0]-1)
        list_options.append(options)
    return max(list_options)


def get_list_positive_instruction_txt(list_instructions_str):
    new_list_positive_instruction_txt = [i for i in list_instructions_str if "A" in i]
    return new_list_positive_instruction_txt


def get_all_follow_chain_of_rules(list_positive_instruction_txt, dict_instructions, list_instructions_str):
    sum_options_instruction = 0
    for instruction_txt in list_positive_instruction_txt:
        options_instruction = follow_chain_of_rules(instruction_txt, dict_instructions, list_instructions_str)
        sum_options_instruction += options_instruction
        print(options_instruction)
    return sum_options_instruction

# Неверно считает на больших данных а на тестовых верно
t1 = time.time()
# diapason_detail = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}
# options_one_instruction = follow_chain_of_rules(work_processes_str[0],work_processes, work_processes_str)
list_positive_instruction_str = get_list_positive_instruction_txt(work_processes_str)
sum_options = get_all_follow_chain_of_rules(list_positive_instruction_str,work_processes, work_processes_str)
# modern_diapason_by_processes(work_processes["px"], diapason_detail, "A")
t2 = time.time()
print(f"Решение задания 2: {sum_options}")
print(f"время {t2-t1}")