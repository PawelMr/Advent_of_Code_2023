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
    matches = tuple(re.finditer(pattern, string))
    substitutions_list = tuple(i.start() for i in matches)
    return substitutions_list


# def add_index_substitutions_list(list_element):
#     for element in list_element:
#         substitutions_list = get_index_substitutions_list(element[0])
#         element.append(substitutions_list)


def split_string(list_str):
    list_list_str = []
    for str in list_str:
        element = str.split(' ')
        element[1] = disassemble_into_numbers(element[1])
        list_list_str.append(element)
    return list_list_str


def get_new_list_data_sheet(list_element):
    new_list_element = []
    old_list_element = copy.deepcopy(list_element)
    for element in old_list_element:
        list_new_string = [element[0] for i in range(5)]
        new_string = "?".join(list_new_string)
        new_cart = element[1]*5
        new_list_element.append([new_string, new_cart])
    return new_list_element


def checking_number_of_options(string, verification_block, index_string=0, index_of_verification_block=0,
                               number_of_characters_in_verification_block=0):
    key = (index_string, index_of_verification_block, number_of_characters_in_verification_block)
    if key in dict_iteration_of_recursion:
        return dict_iteration_of_recursion[key]
    number_of_options = 0
    if index_string == len(string):
        if (index_of_verification_block == len(verification_block) - 1 and
                number_of_characters_in_verification_block == verification_block[index_of_verification_block]):
            return 1
        elif (index_of_verification_block == len(verification_block) and
                number_of_characters_in_verification_block == 0):
            return 1
        else:
            return 0
    else:

        if string[index_string] in [".", "?"]:
            if number_of_characters_in_verification_block == 0:
                number_of_options += checking_number_of_options(string, verification_block, index_string+1,
                                                                index_of_verification_block,
                                                                number_of_characters_in_verification_block)
            elif (number_of_characters_in_verification_block > 0
                  and number_of_characters_in_verification_block == verification_block[index_of_verification_block]
                  and index_of_verification_block <len(verification_block)):
                number_of_options += checking_number_of_options(string, verification_block, index_string + 1,
                                                                index_of_verification_block+1,
                                                                0)
        if string[index_string] in ["#", "?"]:
            if (index_of_verification_block <len(verification_block)
                    and number_of_characters_in_verification_block < verification_block[index_of_verification_block]):
                number_of_options += checking_number_of_options(string, verification_block, index_string + 1,
                                                                index_of_verification_block,
                                                                number_of_characters_in_verification_block+1)

        dict_iteration_of_recursion.update({key:number_of_options})

    return number_of_options


def get_sum_options(list_element):
    all_sum = 0
    for element in list_element:
        dict_iteration_of_recursion.clear()
        all_sum += checking_number_of_options(*element)
        print()
    return all_sum


dict_iteration_of_recursion = {}
list_data_sheet = split_string(list_txt)
sum_options = get_sum_options(list_data_sheet)
print(f"Решение задания 1: {sum_options}")


new_list_data_sheet = get_new_list_data_sheet(split_string(list_txt))
sum_options = get_sum_options(new_list_data_sheet)
print(f"Решение задания 1: {sum_options}")
# a = checking_number_of_options(*list_data_sheet[1])
# for i in range(6):
#     print(checking_number_of_options(*new_list_data_sheet[i]))

# list(product('#.', repeat=len(i[2])))
print()