import copy
import re
with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


def big_disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = int("".join(number_txt_list))
    return number_list


def create_dict_distance(list_string, big=False):
    if big:
        time = [big_disassemble_into_numbers([i for i in list_string if i.startswith("Time")][0])]
        distance = [big_disassemble_into_numbers([i for i in list_string if i.startswith("Distance")][0])]
    else:
        time = disassemble_into_numbers([i for i in list_string if i.startswith("Time")][0])
        distance = disassemble_into_numbers([i for i in list_string if i.startswith("Distance")][0])
    dict_old_result_txt = {"Time": time,
                           "Distance": distance}
    return dict_old_result_txt


dict_old_result_race = create_dict_distance(list_txt)


def decompose_into_product_numbers(number):
    list_product_numbers = []
    for i in range(1, number):
        list_product_numbers.append(number*i - i*i)
    return list_product_numbers


dict_new_result_race = dict(dict_old_result_race)
dict_new_result_race.update({"NewDistance": [decompose_into_product_numbers(i) for i in dict_old_result_race["Time"]]})
dict_new_result_race.update({"WinDistance": []})
for index, value in enumerate(dict_new_result_race["NewDistance"]):
    list_win_result = [i for i in value if i> dict_new_result_race["Distance"][index]]
    dict_new_result_race["WinDistance"].append(list_win_result)

import math
sum_winning_option = math.prod([len(i) for i in dict_new_result_race["WinDistance"]])

print(f"Решение задания 1: {sum_winning_option}")

big_dict_old_result_race = create_dict_distance(list_txt, True)

big_dict_new_result_race = dict(big_dict_old_result_race)
big_dict_new_result_race.update({"NewDistance":
                                     [decompose_into_product_numbers(i) for i in big_dict_old_result_race["Time"]]})
big_dict_new_result_race.update({"WinDistance": []})
for index, value in enumerate(big_dict_new_result_race["NewDistance"]):
    big_list_win_result = [i for i in value if i > big_dict_new_result_race["Distance"][index]]
    big_dict_new_result_race["WinDistance"].append(big_list_win_result)
big_sum_winning_option = math.prod([len(i) for i in big_dict_new_result_race["WinDistance"]])

print(f"Решение задания 2: {big_sum_winning_option}")
