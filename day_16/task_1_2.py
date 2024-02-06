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


def determine_get_from_point(symbol, direction):
    movement_options = {
        "-": {">": ((0, 1, ">"),),
              "<": ((0, -1, "<"),),
              "^": ((0, 1, ">"), (0, -1, "<")),
              "v": ((0, 1, ">"), (0, -1, "<"))},
        "|": {">": ((-1, 0, "^"), (1, 0, "v")),
              "<": ((-1, 0, "^"), (1, 0, "v")),
              "^": ((-1, 0, "^"),),
              "v": ((1, 0, "v"),)},
        "\\": {">": ((1, 0, "v"),),
               "<": ((-1, 0, "^"),),
               "^": ((0, -1, "<"),),
               "v": ((0, 1, ">"),)},
        "/": {"<": ((1, 0, "v"),),
              ">": ((-1, 0, "^"),),
              "v": ((0, -1, "<"),),
              "^": ((0, 1, ">"),)},
        ".": {">": ((0, 1, ">"),),
              "<": ((0, -1, "<"),),
              "^": ((-1, 0, "^"),),
              "v": ((1, 0, "v"),)},
    }
    return movement_options[symbol][direction]

def check_beam_repetition(next_point, direction, dict_ray_of_light:dict):
    if dict_ray_of_light.get(next_point):
        if direction in dict_ray_of_light[next_point]:
            return True
        else:
            dict_ray_of_light[next_point] = direction + dict_ray_of_light[next_point]
    else:
        dict_ray_of_light.update({next_point:direction})
    return False


def seek_path_of_light(mirror_map, next_point, direction, dict_ray_of_light):
    can_move = True
    while can_move:
        if next_point[0] < 0 \
                or next_point[0] > len(mirror_map)-1 \
                or next_point[1] < 0 \
                or next_point[1] > len(mirror_map[0])-1:
            can_move = False
            continue
        if check_beam_repetition(next_point, direction, dict_ray_of_light):
            can_move = False
            continue
        symbol = mirror_map[next_point[0]][next_point[1]]
        next_step = determine_get_from_point(symbol, direction)
        if len(next_step) == 1:
            next_point = (next_point[0]+next_step[0][0], next_point[1]+next_step[0][1])
            direction = next_step[0][2]
        if len(next_step) == 2:
            for i in range(len(next_step)):
                next_point = (next_point[0] + next_step[i][0], next_point[1] + next_step[i][1])
                direction = next_step[i][2]
                seek_path_of_light(mirror_map, next_point, direction, dict_ray_of_light)
            can_move = False
            continue


t1 = time.time()
full_map = tuple(parser_map(i)for i in list_txt)
dict_ray = {}
seek_path_of_light(full_map, (0, 0), ">", dict_ray)
sum_ray = len(dict_ray)
t2 = time.time()
print(f"Решение задания 1: {sum_ray}")
print(f"время {t2-t1}")


def check_all_starting_points(mirror_map):
    list_sum_ray = []
    horizontal_length = len(mirror_map[0])
    vertical_length = len(mirror_map)
    for i in range(vertical_length):
        dict_ray_of_light_left = {}
        seek_path_of_light(mirror_map, (i, 0), ">", dict_ray_of_light_left)
        dict_ray_of_light_right = {}
        seek_path_of_light(mirror_map, (i, horizontal_length-1), "<", dict_ray_of_light_right)
        list_sum_ray.append(len(dict_ray_of_light_left))
        list_sum_ray.append(len(dict_ray_of_light_right))
    for i in range(horizontal_length):
        dict_ray_of_light_up = {}
        seek_path_of_light(mirror_map, (0, i), "v", dict_ray_of_light_up)
        dict_ray_of_light_right_down = {}
        seek_path_of_light(mirror_map, (vertical_length-1, i), "^", dict_ray_of_light_right_down)
        list_sum_ray.append(len(dict_ray_of_light_up))
        list_sum_ray.append(len(dict_ray_of_light_right_down))
    return list_sum_ray


t1 = time.time()
full_map = tuple(parser_map(i)for i in list_txt)
list_sum = check_all_starting_points(full_map)
max_ray = max(list_sum)
t2 = time.time()
print(f"Решение задания 2: {max_ray}")
print(f"время {t2-t1}")












