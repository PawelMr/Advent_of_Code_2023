import copy
import re
import collections
import time
import math

with open("test.txt", mode="r", encoding="utf-8") as test_file:
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
    return movement_options[direction]


def get_direction(step):
    movement_options = {
        (0, 1): ">",
        (0, -1): "<",
        (-1, 0): "^",
        (1, 0): "v"
    }
    return movement_options[step]

def find_possible_directions(point, direction, steps_taken, m, n):
    """

    :param point: положение сейчас
    :param direction: направление от куда пришли
    :param steps_taken:  уже сделано шагов
    :param m: размер матрицы по вертикали
    :param n: размер матрицы по горизонтали
    :return:
    """
    # all_options = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    possible_directions = []
    if point[0] != 0:
        possible_directions.append((-1, 0))
    if point[0] != m-1:
        possible_directions.append((1, 0))
    if point[1] != 0:
        possible_directions.append((0, -1))
    if point[1] != n-1:
        possible_directions.append((0, 1))
    step_back = get_where_from(direction)
    if step_back and step_back in possible_directions:
        possible_directions.remove(step_back)
    if steps_taken == 3:
        step_forward = get_where(direction)
        if step_forward in possible_directions:
            possible_directions.remove(step_forward)

    return possible_directions


def check_dict_point_in_map(key_1,key_2,dict_point_in_map, sum_heat_loss):
    if (dict_point_in_map.get(key_1)
            and dict_point_in_map[key_1].get(key_2)
            and dict_point_in_map[key_1][key_2] < sum_heat_loss):
        return False
    if dict_point_in_map.get(key_1):
        dict_point_in_map[key_1].update({key_2: sum_heat_loss})
    else:
        dict_point_in_map.update({key_1: {key_2: sum_heat_loss}})
    return True


def take_step_on_map(point, direction, steps_taken, sum_heat_loss, ful_map):
    dict_min_sum_in_point = {}
    list_new_point = get_new_point(point, direction, steps_taken, sum_heat_loss, ful_map, dict_min_sum_in_point)
    while list_new_point:
        list_new_point.extend(get_new_point(*list_new_point[0], ful_map, dict_min_sum_in_point))
        list_new_point.pop(0)
    return dict_min_sum_in_point



def get_new_point(point, direction, steps_taken, sum_heat_loss, ful_map, dict_min_sum_in_point):
    m, n = len(ful_map), len(ful_map[0])
    list_new_point = []
    for new_step in find_possible_directions(point, direction, steps_taken, m, n):
        new_direction = get_direction(new_step)
        if not direction or new_direction == direction:
            new_steps_taken = steps_taken+1
        else:
            new_steps_taken = 1
        new_point = (point[0] + new_step[0], point[1] + new_step[1])
        new_sum_heat_loss = sum_heat_loss + ful_map[new_point[0]][new_point[1]]
        key_1 = point
        key_2 = (direction, steps_taken)
        if check_dict_point_in_map(key_1, key_2, dict_min_sum_in_point, sum_heat_loss):
            list_new_point.append((new_point, new_direction,new_steps_taken,new_sum_heat_loss))
    return list_new_point







# !!!!!!!!!!!!!на больших данных время неадекватное
t1 = time.time()
map_city = tuple(parser_map(i)for i in list_txt)
list_sum = []
dict_min_in_point = take_step_on_map((0, 0), None, 0, 0, map_city)
point_final = dict_min_in_point[(len(map_city)-1, len(map_city[0])-1)]
list_final_heat_loss = [j for i, j in point_final.items()]
t2 = time.time()
print(f"Решение задания 2: {min(list_final_heat_loss)}")
print(f"время {t2-t1}")



