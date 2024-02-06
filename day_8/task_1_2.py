import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_map(str_element_map):
    matches = re.findall(r"\b([a-zA-Z0-9]+)\b", str_element_map)
    return matches


def get_dict_map_nodes(list_map_nodes):
    dict_map = {}
    for i in list_map_nodes:
        if dict_map.get(i[0]):
            raise Exception(f"дублирующий по первой координате элемент карты {i}")
        else:
            dict_map.update({i[0]: [i[1], i[2]]})
    return dict_map


def step_on_map_once(dict_map, start_element, step_direction):
    if not dict_map.get(start_element):
        raise Exception(f"в карте нет координат {start_element}")
    else:
        finish_options = dict_map[start_element]
        if step_direction == "R":
            finish_element = finish_options[1]
        elif step_direction == "L":
            finish_element = finish_options[0]
        else:
            raise Exception(f"шаг в никуда {step_direction}")
    return finish_element


def follow_map(dict_map, start_element, string_step_direction, desired_finish, steps_have_taken=0):
    point_on_map = start_element
    start_boll = True
    for i in string_step_direction:
        if not desired_finish(point_on_map) and not start_boll:
            break
        start_boll = False
        point_on_map = step_on_map_once(dict_map, point_on_map, i)
        steps_have_taken += 1
    return point_on_map, steps_have_taken


def find_length_path(dict_map,start_element,cycle_condition):
    steps_have_taken_by_map = 0
    point_on_map_now = start_element
    while cycle_condition(point_on_map_now) or not bool(steps_have_taken_by_map):
        point_on_map_now, steps_taken_now = follow_map(dict_map, point_on_map_now,
                                                       movement_instructions, cycle_condition,
                                                       steps_have_taken_by_map)
        steps_have_taken_by_map = steps_taken_now
        print(f"уже сделали шагов {steps_have_taken_by_map}")
    return point_on_map_now, steps_have_taken_by_map


movement_instructions = parser_map(list_txt[0])[0]
map_nodes = [parser_map(i) for i in list_txt[1:] if i != "\n"]
dict_map_nodes = get_dict_map_nodes(map_nodes)

t1 = time.time()
start_element_map = "AAA"
exit_condition = lambda x: x != "ZZZ"
print(f"Решение задания 1: {find_length_path(dict_map_nodes,start_element_map, exit_condition)[1]}")
f1 = time.time()
print(f"время {f1-t1}")

t2 = time.time()


list_start_element_map = [i for i in dict_map_nodes if i[2] == "A"]
exit_condition_2 = lambda x: x[2] != "Z"
return_condition = lambda x: x[2] != "A"
dict_start_to_finish ={}
dict_finish_to_two_finish ={}

for i in list_start_element_map:
    finish_point, steps_to_exit = find_length_path(dict_map_nodes, i, exit_condition_2)
    dict_start_to_finish.update({finish_point: steps_to_exit})
    two_finish_point, steps_to_two_finish = find_length_path(dict_map_nodes, finish_point, exit_condition_2)
    dict_finish_to_two_finish.update({two_finish_point: steps_to_two_finish})

total_multiple = 1
for key, value in dict_finish_to_two_finish.items():
    total_multiple = (total_multiple * value) // math.gcd(total_multiple, value)

f2 = time.time()



print(f"Решение задания 2: {total_multiple}")
print (f"время {f2-t2}")
