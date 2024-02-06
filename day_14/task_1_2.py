import copy
import re
import collections
import time
import math


with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()

def split_list_string(list_string):
    new_matrix = []
    for string in list_string:
        new_matrix.append(list(string.replace("\n", "")))
    return new_matrix

def matrix_transposition(old_matrix):
    new_matrix = [[0 for j in range(len(old_matrix))]for i in range(len(old_matrix[0]))]
    for i in range(len(old_matrix)):
        for j in range(len(old_matrix[i])):
            new_matrix[j][i] = old_matrix[i][j]
    return new_matrix


def move_stones_to_left(list_stones):
    end_point = 0
    for i in range(len(list_stones)):
        if list_stones[i] == "#" or (list_stones[i] == "O" and i == end_point):
            end_point = i+1
        elif list_stones[i] == "O":
            list_stones[end_point] = "O"
            end_point += 1
            list_stones[i] = "."


def move_list_stones_to_left(matrix):
    for list_element in matrix:
        move_stones_to_left(list_element)


def calculate_weight_of_stones(list_stones):
    max_weight = len(list_stones)
    sum_weight = 0
    for i in range(len(list_stones)):
        if list_stones[i] == "O":
            sum_weight += max_weight - i
    return sum_weight


def calculate_weight_of_list_stones(matrix):
    list_sum = []
    for list_element in matrix:
        list_sum.append(calculate_weight_of_stones(list_element))
    return list_sum


def flip_matrix_vertically(matrix):
    for list_element in matrix:
        list_element.reverse()


t1 = time.time()
map_of_stones = split_list_string(list_txt)
transposition_map_of_stones = matrix_transposition(map_of_stones)
move_list_stones_to_left(transposition_map_of_stones)
list_sum_stones = calculate_weight_of_list_stones(transposition_map_of_stones)
answer = sum(list_sum_stones)
t2 = time.time()
print(f"Решение задания 1: {answer}")
print(f"время {t2-t1}")


def run_one_cycle(matrix):
    # на сервер слева
    new_matrix = matrix_transposition(matrix)
    move_list_stones_to_left(new_matrix)
    new_matrix = matrix_transposition(new_matrix)
    # запад слева

    move_list_stones_to_left(new_matrix)
    # юг на лево
    new_matrix = matrix_transposition(new_matrix)
    flip_matrix_vertically(new_matrix)
    move_list_stones_to_left(new_matrix)
    flip_matrix_vertically(new_matrix)
    new_matrix = matrix_transposition(new_matrix)
    # восток слева

    flip_matrix_vertically(new_matrix)
    move_list_stones_to_left(new_matrix)
    flip_matrix_vertically(new_matrix)
    return new_matrix


def perform_several_cycles(matrix, len_several):
    # if len_several > 3:
    #     len_several = 3 + (len_several - 3) % 7
    list_matrix = []
    found_repeat = False
    matrix_repeat=None
    index_cickl = 1
    list_number_repeat = []
    while index_cickl<len_several:
        matrix = run_one_cycle(matrix)
        if not found_repeat:
            list_matrix.append( copy.deepcopy(matrix))

        if matrix in list_matrix and list_matrix.index(matrix)+1 != index_cickl and not found_repeat:
            found_repeat = True
            number_repeat = list_matrix.index(matrix)+1
            matrix_repeat = matrix
        if matrix == matrix_repeat and found_repeat:
            print(f"повторили {number_repeat} цикл на {index_cickl}")
            list_number_repeat.append(index_cickl)
            if len(list_number_repeat) == 2:
                repetition_length = list_number_repeat[1] - list_number_repeat[0]
                print(f"повторили через {repetition_length}")
                index_cickl = index_cickl + ((len_several-index_cickl)//repetition_length)*repetition_length
                print(f"прыгнули на {index_cickl}")
                continue

        index_cickl += 1
    print(index_cickl)
    return matrix


def calculate_above_weight_of_list_stones(matrix):
    list_sum = []
    max_multiplier = len(matrix)
    for i in range(len(matrix)):
        list_sum.append(matrix[i].count("O")*(max_multiplier-i))
    return list_sum

t1 = time.time()
# last_matrix = perform_several_cycles(map_of_stones, 400)
last_matrix = perform_several_cycles(map_of_stones, 1000000000)
list_2_sum_stones = calculate_above_weight_of_list_stones(last_matrix)

t2 = time.time()
# print(f"Решение задания 1: {answer}")
print(f"Решение задания 2: {sum(list_2_sum_stones)}")
print(f"время {t2-t1}")
print()
