import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    return tuple(int(i) for i in str_element_map)


def get_where_from(direction):
    movement_options = {
        ">": (0, -1),
        "<": (0, 1),
        "^": (1, 0),
        "v": (-1, 0)
    }
    return movement_options.get(direction, None)


def get_where(direction):
    movement_options = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0)
    }
    return movement_options.get(direction, None)


def get_direction(step):
    movement_options = {
        (0, 1): ">",
        (0, -1): "<",
        (-1, 0): "^",
        (1, 0): "v"
    }
    return movement_options[step]

def find_possible_directions(point, direction, steps_taken, m, n, min_way = 1, max_way= 3):
    """

    :param point: положение сейчас
    :param direction: направление от куда пришли
    :param steps_taken:  уже сделано шагов
    :param m: размер матрицы по вертикали
    :param n: размер матрицы по горизонтали
    :param min_way: минимальный путь до поворота
    :param max_way: максимальный путь до поворота
    :return:
    """
    all_options = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    possible_directions = []
    step_back = get_where_from(direction)
    step_forward = get_where(direction)
    for options in all_options:
        if step_back != options:
            start_taken = min_way if step_forward != options else steps_taken + min_way
            for i in range(start_taken, max_way+1):
                y = options[0] * i
                x = options[1] * i
                if 0 <= point[0] +y <= m - 1 and 0 <= point[1] + x <= n - 1:
                    long_step = i if step_forward != options else i - steps_taken
                    possible_directions.append((options[0], options[1], long_step, i))
    return possible_directions


def check_dict_point_in_map(key_1,key_2,dict_point_in_map, sum_heat_loss):
    if (dict_point_in_map.get(key_1)
            and dict_point_in_map[key_1].get(key_2)
            and dict_point_in_map[key_1][key_2] <= sum_heat_loss):
        return False
    if dict_point_in_map.get(key_1):
        dict_point_in_map[key_1].update({key_2: sum_heat_loss})
    else:
        dict_point_in_map.update({key_1: {key_2: sum_heat_loss}})
    return True


def get_increase_heat_loss(point, step,step_count, ful_map):
    increase_heat_loss = 0
    for i in range(step_count):
        point = (point[0]+step[0], point[1]+step[1])
        increase_heat_loss += ful_map[point[0]][point[1]]
    return point, increase_heat_loss

def get_new_point(ful_map, dict_min_sum_in_point, min_way = 1, max_way= 3):
    m, n = len(ful_map), len(ful_map[0])
    flag = True
    while flag:
        flag = False
        for y in range(m):
            for x in range(n):
                key_1 = (y, x)
                variants = dict_min_sum_in_point.get(key_1,[])
                for variant in variants:
                    list_next_step = find_possible_directions(key_1, *variant, m, n, min_way, max_way)
                    for next_step in list_next_step:
                        step = (next_step[0], next_step[1])
                        step_length = next_step[2]
                        number_step = next_step[3]
                        step_direction = get_direction(step)
                        key_2 = (step_direction, number_step)
                        new_key_1, increase_heat_loss = get_increase_heat_loss(key_1, step, step_length, ful_map)
                        sum_heat_loss = dict_min_sum_in_point[key_1][variant] + increase_heat_loss
                        mini_flag = check_dict_point_in_map(new_key_1, key_2, dict_min_sum_in_point, sum_heat_loss)
                        flag = mini_flag or flag
    return dict_min_sum_in_point











t1 = time.time()
map_city = tuple(parser_map(i)for i in list_txt)
list_sum = []
dict_min_in_point = {(0, 0): {(None, 0): 0}}
dict_min_in_point = get_new_point(map_city,dict_min_in_point)

point_final = dict_min_in_point[(len(map_city)-1, len(map_city[0])-1)]
list_final_heat_loss = [j for i, j in point_final.items()]
t2 = time.time()
print(f"Решение задания 1: {min(list_final_heat_loss)}")
print(f"время {t2-t1}")


t1 = time.time()
map_city = tuple(parser_map(i)for i in list_txt)
list_sum = []
dict_min_in_point = {(0, 0): {(None, 0): 0}}
dict_min_in_point = get_new_point(map_city,dict_min_in_point, min_way=4,max_way=10)

point_final = dict_min_in_point[(len(map_city)-1, len(map_city[0])-1)]
list_final_heat_loss = [j for i, j in point_final.items()]
t2 = time.time()
print(f"Решение задания 2: {min(list_final_heat_loss)}")
print(f"время {t2-t1}")



