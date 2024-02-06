import copy
import re
import collections
import time
import math


with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_str(string):
    matches = re.findall(r"\b([a-zA-Z0-9]+)\b", string)
    return matches


def get_list_of_sequences(string: str):
    string=string.replace("\n", "")
    new_list_sequences = string.split(",")
    return new_list_sequences


def convert_str_to_list_ascii(string: str):
    new_list_ascii = [ord(i) for i in string]
    return new_list_ascii


def convert_list_str_to_list_ascii(list_string:list):
    new_list_sequences_ascii = [convert_str_to_list_ascii(i) for i in list_string]
    return new_list_sequences_ascii


def execute_algorithm(start_list_ascii):
    new_number_algorithm = 0
    for i in start_list_ascii:
        new_number_algorithm += i
        new_number_algorithm = new_number_algorithm * 17
        new_number_algorithm = new_number_algorithm % 256
    return new_number_algorithm


def execute_list_algorithm(list_start_list_ascii):
    new_list_number_algorithm = [execute_algorithm(i) for i in list_start_list_ascii]
    return new_list_number_algorithm


t1 = time.time()
list_sequences = get_list_of_sequences(list_txt[0])
list_sequences_ascii = convert_list_str_to_list_ascii(list_sequences)
list_number_algorithm = execute_list_algorithm(list_sequences_ascii)
print(f"Решение задания 1: {sum(list_number_algorithm)}")
t2 = time.time()
print(f"время {t2-t1}")


def identify_box(string: str):
    return execute_algorithm(convert_str_to_list_ascii(string))


def identify_lens(string: str):
    add_lens = True if "=" in string else False
    parser_string = parser_str(string)
    label = parser_string[0]
    box = identify_box(label)
    focus = parser_string[-1] if add_lens else None
    return box, add_lens, label, focus


def execute_algorithm_hashmap(i_box, add_lens,  label, focus, dict_ful_box):
    box = dict_ful_box[i_box]
    index_lens_in_box = None
    for i in range(len(box)):
        if label == box[i][0]:
            index_lens_in_box = i
            break
    if add_lens:
        if not index_lens_in_box is None:
            box[index_lens_in_box] = [label, focus]
        else:
            box.append([label, focus])
    else:
        if not index_lens_in_box is None:
            box.pop(index_lens_in_box)


def calculating_focusing_ability(dict_ful_box):
    list_focusing_ability = []
    for numbers_box, box in dict_ful_box.items():
        for index_lens in range(len(box)):
            list_focusing_ability.append((1+numbers_box)*(1+index_lens) * int(box[index_lens][1]))
    return list_focusing_ability


t1 = time.time()
lisl_after = [identify_lens(i)for i in list_sequences]
dict_boxs = {i: [] for i in range(256)}

for after in lisl_after:
    execute_algorithm_hashmap(*after, dict_boxs)

list_focusing = calculating_focusing_ability(dict_boxs)

print(f"Решение задания 1: {sum(list_focusing)}")
t2 = time.time()
print(f"время {t2-t1}")

