import re

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def find_index(start_index,end_index, index_string):
    max_index_string_file = len(list_txt) - 1
    max_index_string = len(list_txt[index_string]) - 1
    list_index_string_check = [index_string]
    if index_string > 0:
        list_index_string_check.append(index_string - 1)
    if index_string < max_index_string_file:
        list_index_string_check.append(index_string + 1)

    if start_index > 0:
        start_index -= 1
    if end_index < max_index_string:
        end_index += 1
    return start_index, end_index, list_index_string_check


def find_symbol(number, index_string):
    symbol_check = r'[^0-9.\d]'

    start_index = number.start()
    end_index = number.end()

    start_index, end_index, list_index_string_check = find_index(start_index,end_index, index_string)

    for index_str_symbol in list_index_string_check:
        try:
            symbol = re.findall(symbol_check, list_txt[index_str_symbol][start_index: end_index])
        except:
            return Exception(f"с индексом беда строка {index_string}, срез [{start_index}: {end_index}]")
        if symbol:
            return int(number.group(1))
    return None


def find_numbers(list_index_string_check, asterisk_index,asterisk_index_end):
    number_pattern = r'(\d+)'
    list_numbers = []
    for index_string in list_index_string_check:
        matches = list(re.finditer(number_pattern, list_txt[index_string]))
        if matches:
            for match in matches:
                start_index = match.start()
                end_index = match.end()
                if start_index <= asterisk_index_end and asterisk_index <= end_index:
                    list_numbers.append(int(match.group(1)))
    return list_numbers


def looking_asterisk(match, index_string):
    figure_check = r'\d+'
    asterisk_index = match.start()
    asterisk_index_end = match.end()
    gear_ratio = 0
    start_index, end_index, list_index_string_check = find_index(asterisk_index, asterisk_index_end, index_string)

    list_ful_figure_check = []
    for index_str_figure in list_index_string_check:
        list_figure = re.findall(figure_check, list_txt[index_str_figure][start_index: end_index])
        if list_figure:
            list_ful_figure_check.extend(list_figure)
    if len(list_ful_figure_check) == 2:
        list_numbers = find_numbers(list_index_string_check, asterisk_index, asterisk_index_end)
        gear_ratio = list_numbers[0]*list_numbers[1]
    return gear_ratio


import time




list_number = []
for index_string in range(len(list_txt)):
    pattern = r'(\d+)'
    matches = list(re.finditer(pattern, list_txt[index_string]))
    if matches:
        for match in matches:
            number = find_symbol(match, index_string)
            if number:
                list_number.append(number)
print(f"Решение задания 1: {sum(list_number)}")

summ_gear_ratio = 0
for index_string in range(len(list_txt)):
    pattern = r'\*'
    matches = list(re.finditer(pattern, list_txt[index_string]))
    if matches:
        for match in matches:
            gear_ratio = looking_asterisk(match, index_string)
            summ_gear_ratio += gear_ratio

print(f"Решение задания 2: {summ_gear_ratio}")


