import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    return tuple(str_element_map)


def find_coordinates_s(list_map_line):
    for index_map_line in range(len(list_map_line)):
        for index_point_map in range(len(list_map_line[index_map_line])):
            if list_map_line[index_map_line][index_point_map] == "S":
                return (index_map_line, index_point_map,), "S"


def determine_get_from_point(symbol):
    movement_options = {
        "S": ((0, 1), (1, 0), (0, -1), (-1, 0)),
        "-": ((0, 1),  (0, -1)),
        "|": ((1, 0), (-1, 0)),
        "L": ((0, 1), (-1, 0)),
        "7": ((0, -1), (1, 0)),
        "J": ((0, -1), (-1, 0)),
        "F": ((0, 1), (1, 0)),
        ".": ()
    }
    return movement_options[symbol]


def check_if_there_passage(point_start_coordinates, direction, list_map_line):
    new_symbol = list_map_line[point_start_coordinates[0]+direction[0]][point_start_coordinates[1]+direction[1]]
    new_variants = determine_get_from_point(new_symbol)
    for new_variant in new_variants:
        if new_variant[0]+direction[0] == 0 and new_variant[1]+direction[1] == 0:
            return True
    return False


def find_start_way(point_start, list_map_line):
    variants = determine_get_from_point(point_start[1])
    for variant in variants:
        if check_if_there_passage(point_start[0], variant, list_map_line):
            next_point_index_1 = point_start[0][0]+variant[0]
            next_point_index_2 = point_start[0][1]+variant[1]
            next_point = ((next_point_index_1,next_point_index_2),list_map_line[next_point_index_1][next_point_index_2])
            return next_point


def find_ful_way(list_point, list_map_line):
    while True:
        list_variants = determine_get_from_point(list_point[-1][1])
        for variant in list_variants:
            next_point_index_1 = list_point[-1][0][0] + variant[0]
            next_point_index_2 = list_point[-1][0][1] + variant[1]
            if list_point[-2][0] != (next_point_index_1, next_point_index_2):
                next_point = ((next_point_index_1, next_point_index_2),
                              list_map_line[next_point_index_1][next_point_index_2])
                break
        if next_point == list_point[0]:
            break
        else:
            list_point.append(next_point)


def find_inner_points(line_point, index_string, dict_ful_way):
    entrance = False
    turn = False
    list_point_entrance = []
    for i in range(len(line_point)):
        symbol_way = dict_ful_way.get((index_string, i))
        if symbol_way:
            if symbol_way == "|":
                entrance = not entrance
                continue
            if symbol_way not in "|-" and not turn:
                turn = symbol_way
                continue
            if symbol_way not in "|-" and turn:
                if determine_get_from_point(symbol_way)[1][0]+determine_get_from_point(turn)[1][0] == 0:
                    entrance = not entrance
                turn = False
                continue
        if entrance and not symbol_way:
            list_point_entrance.append(((index_string, i), line_point[i]))
    return list_point_entrance


def replace_s(point_s, point_next, point_previous):
    direction_1 = (point_next[0][0]-point_s[0][0],point_next[0][1]-point_s[0][1])
    direction_2 = (point_previous[0][0] - point_s[0][0], point_previous[0][1] - point_s[0][1])
    turn = (direction_1[0]+direction_2[0], direction_1[1]+direction_2[1])
    if turn == (1, 1):
        new_symbol = "F"
    if turn == (-1, 1):
        new_symbol = "L"
    if turn == (1, -1):
        new_symbol = "7"
    if turn == (-1, -1):
        new_symbol = "J"
    if turn == (0, 0):
        if direction_1[0] == 0:
            new_symbol = "-"
        else:
            new_symbol = "|"
    return new_symbol


t1 = time.time()
full_map = tuple(parser_map(i) for i in list_txt)
coordinates_s = find_coordinates_s(full_map)
two_symbol = find_start_way(coordinates_s, full_map)
list_way = [coordinates_s, two_symbol]
find_ful_way(list_way, full_map)
t2 = time.time()
print(f"Решение задания 1: {len(list_way)/2}")
print(f"время {t2-t1}")

t1 = time.time()
new_symbol_s = replace_s(list_way[0], list_way[1], list_way[-1])
dict_way = {i[0]: i[1] if i[1] != "S" else new_symbol_s for i in list_way}
ful_list_point_entrance = []
find_inner_points(full_map[2], 2, dict_way)
for index_list_map in range(len(full_map)):
    ful_list_point_entrance.extend(find_inner_points(full_map[index_list_map], index_list_map, dict_way))
t2 = time.time()
print(f"Решение задания 2: {len(ful_list_point_entrance)}")
print(f"время {t2-t1}")
