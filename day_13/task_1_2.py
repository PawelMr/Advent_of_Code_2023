import copy
import re
import collections
import time
import math
import difflib

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def get_list_matrices(list_txt):
    new_list_matrices = [[]]
    index_matrix = 0
    for i in list_txt:
        if i != "\n":
            new_list_matrices[index_matrix].append(i.replace("\n",""))
        else:
            new_list_matrices.append([])
            index_matrix +=1
    return new_list_matrices


def matrix_transposition(old_matrix):
    new_matrix = [[0 for j in range(len(old_matrix))]for i in range(len(old_matrix[0]))]
    for i in range(len(old_matrix)):
        for j in range(len(old_matrix[i])):
            new_matrix[j][i] = old_matrix[i][j]
    for index_string in range(len(new_matrix)):
        new_matrix[index_string] = "".join(new_matrix[index_string])
    return new_matrix


def get_number_of_discrepancies(list_one, list_two):
    number_of_discrepancies = 0
    for i in range(len(list_one)):
        for j in range(len(list_one[i])):
            if list_one[i][j] != list_two[i][j]:
                number_of_discrepancies += 1
    return number_of_discrepancies


def find_mirrors_in_matrix(matrix, fix_symbol=False):
    list_index_mirrors = []
    for i in range(1,len(matrix)):
        reflection_length = min([len(matrix[:i]), len(matrix[i:])])
        number_of_discrepancies = get_number_of_discrepancies(matrix[i - reflection_length:i],
                                                              matrix[i+reflection_length-1:i-1:-1])
        if not fix_symbol and number_of_discrepancies == 0:
            return i
        if fix_symbol and number_of_discrepancies == 1:
            return i

        # if matrix[i-reflection_length:i] == matrix[i+reflection_length-1:i-1:-1]:
        #     return i
        # elif fix_symbol:
        #     number_of_discrepancies = get_number_of_discrepancies(matrix[i-reflection_length:i],
        #                                                           matrix[i+reflection_length-1:i-1:-1])
        #     if number_of_discrepancies ==1:
        #         for j in matrix:
        #             print(j)
        #         print(f"======================================== {i}")
        #         return i
    return None
    #         list_index_mirrors.append(i)
    # return list_index_mirrors


def find_mirrors_in_list_matrix(list_matrices, fix_symbol=False):
    list_mirrors_horizontally =[]
    list_mirrors_vertically = []
    for matrix in list_matrices:
        mirror_horizontal = find_mirrors_in_matrix(matrix, fix_symbol)
        if mirror_horizontal:
            list_mirrors_horizontally.append(mirror_horizontal)
        # list_mirrors_horizontally.extend(find_mirrors_in_matrix(matrix))
        else:
            new_matrix = matrix_transposition(matrix)
            mirror_vertical = find_mirrors_in_matrix(new_matrix, fix_symbol)
        # list_mirrors_vertically.extend(find_mirrors_in_matrix(new_matrix))
            if mirror_vertical:
                list_mirrors_vertically.append(mirror_vertical)
            del new_matrix
    return list_mirrors_horizontally, list_mirrors_vertically


t1 = time.time()
list_field = get_list_matrices(list_txt)
mirrors_horizontally, mirrors_vertically = find_mirrors_in_list_matrix(list_field)
answer = sum(mirrors_horizontally)*100 + sum(mirrors_vertically)
t2 = time.time()
print(f"Решение задания 1: {answer}")
print(f"время {t2-t1}")

t1 = time.time()
mirrors_horizontally, mirrors_vertically = find_mirrors_in_list_matrix(list_field, fix_symbol=True)
answer = sum(mirrors_horizontally)*100 + sum(mirrors_vertically)
t2 = time.time()
print(f"Решение задания 2: {answer}")
print(f"время {t2-t1}")