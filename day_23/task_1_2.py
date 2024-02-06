import copy
import re
import collections
import time
import math

with open("test.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")

    # list_coordinates.sort(key=sort_wan_z_coordinates)
    return str_element_map


def get_new_step(old_step,direction):
    return old_step[0]+direction[0], old_step[1]+direction[1]


def get_content_coordinates(step, ful_map):
    return ful_map[step[0]][step[1]]


def get_variants_movement(last_step, penultimate_step, ful_map):
    ful_variants = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    variants_l = [(0, -1)]
    variants_r = [(0, 1)]
    variants_up = [(-1, 0)]
    variants_d = [(1, 0)]
    match get_content_coordinates(last_step,ful_map):
        case ".":
            now_variants = ful_variants
        case "<":
            now_variants = variants_l
        case ">":
            now_variants = variants_r
        case "v":
            now_variants = variants_d
        case "^":
            now_variants = variants_up
        case value:
            raise Exception(f"Пришла какая то чуш {value}")
    if last_step[0] == 0:
        now_variants.remove((-1, 0))
    new_list_next_step = [get_new_step(last_step, i)
                          for i in now_variants if get_new_step(last_step, i) != penultimate_step
                          and get_content_coordinates(get_new_step(last_step, i), ful_map) != "#"]
    return new_list_next_step


def get_variants_movement_not_slope(last_step, penultimate_step, ful_map):
    now_variants = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if last_step[0] == 0:
        now_variants.remove((-1, 0))
    new_list_next_step = [get_new_step(last_step, i)
                          for i in now_variants if get_new_step(last_step, i) != penultimate_step
                          and get_content_coordinates(get_new_step(last_step, i), ful_map) != "#"]
    return new_list_next_step


def get_variants_path(list_step, ful_map, step_finish):
    list_path = []
    while list_step[-1] != step_finish:
        penultimate_step = list_step[-2] if len(list_step) > 1 else None
        list_next_step = get_variants_movement(list_step[-1], penultimate_step, ful_map)
        if len(list_next_step) == 1:
            if list_next_step[0] not in list_step:
                list_step.append(list_next_step[0])
            else:
                list_step = None
                break
        elif len(list_next_step) == 0:
            list_step = None
            break
        else:
            for variant in list_next_step:
                if variant in list_step:
                    continue
                other_list_step = copy.deepcopy(list_step)
                other_list_step.append(variant)
                list_path.extend(get_variants_path(other_list_step, ful_map, step_finish))
            list_step = None
            break
    if list_step:
        list_path.append(list_step)
    return list_path


def get_variants_path_not_slope(list_step, ful_map, step_finish):
    list_path = []
    while list_step[-1] != step_finish:
        penultimate_step = list_step[-2] if len(list_step) > 1 else None
        list_next_step = get_variants_movement_not_slope(list_step[-1], penultimate_step, ful_map)
        if len(list_next_step) == 1:
            if list_next_step[0] not in list_step:
                list_step.append(list_next_step[0])
            else:
                list_step = None
                break
        elif len(list_next_step) == 0:
            list_step = None
            break
        else:
            for variant in list_next_step:
                if variant in list_step:
                    continue
                other_list_step = copy.deepcopy(list_step)
                other_list_step.append(variant)
                list_path.extend(get_variants_path_not_slope(other_list_step, ful_map, step_finish))
            list_step = None
            break
    if list_step:
        list_path.append(list_step)
    return list_path


# t1 = time.time()
# map_start = [parser_map(i) for i in list_txt]
# point_start = (0, map_start[0].index("."))
# point_finish = (len(map_start)-1, map_start[-1].index("."))
# ful_list_path = get_variants_path([point_start], map_start, point_finish)
# list_path_len = [len(i)-1 for i in ful_list_path]
# max_path = max(list_path_len)
# t2 = time.time()
# print(f"Решение задания 1: {max_path}")
# print(f"время {t2-t1}")

# НЕ адекватно моного времени
t1 = time.time()
map_start = [parser_map(i) for i in list_txt]
point_start = (0, map_start[0].index("."))
point_finish = (len(map_start)-1, map_start[-1].index("."))
ful_list_path = get_variants_path_not_slope([point_start], map_start, point_finish)
list_path_len = [len(i)-1 for i in ful_list_path]
max_path = max(list_path_len)
t2 = time.time()
print(f"Решение задания 2: {max_path}")
print(f"время {t2-t1}")




