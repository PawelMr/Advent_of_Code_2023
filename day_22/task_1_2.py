import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()



sort_wan_z_coordinates = lambda x: x[2]
sort_list_coordinates_z = lambda x: (x[0][2], x[0][0], x[0][1], x[1][0], x[1][1])


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    list_coordinates = str_element_map.split("~")
    list_coordinates = [[int(j) for j in i.split(",")] for i in list_coordinates]
    if (list_coordinates[0][0] > list_coordinates[1][0]
            or list_coordinates[0][1] > list_coordinates[1][1]
            or list_coordinates[0][2] > list_coordinates[1][2]):
        raise Exception(f" Координаты не по возрастанию {list_coordinates}")
    # list_coordinates.sort(key=sort_wan_z_coordinates)
    return list_coordinates


def get_new_coordinates_of_the_top_layer(old_brick, new_brick):
    new_old_list_brick = []
    if old_brick[1][0] - old_brick[0][0] > 0:
        x1 = old_brick[0][0]
        x2 = new_brick[0][0]-1
        x3 = new_brick[1][0]+1
        x4 = old_brick[1][0]
        if x1 <= x2:
            new_old_list_brick.append([[x1, old_brick[0][1], old_brick[0][2]], [x2, old_brick[1][1], old_brick[1][2]]])
        if x3 <= x4:
            new_old_list_brick.append([[x3, old_brick[0][1], old_brick[0][2]], [x4, old_brick[1][1], old_brick[1][2]]])
    elif old_brick[1][1]- old_brick[0][1] > 0:
        y1 = old_brick[0][1]
        y2 = new_brick[0][1] - 1
        y3 = new_brick[1][1] + 1
        y4 = old_brick[1][1]
        if y1 <= y2:
            new_old_list_brick.append([[old_brick[0][0], y1, old_brick[0][2]], [old_brick[0][0], y2, old_brick[1][2]]])
        if y3 <= y4:
            new_old_list_brick.append([[old_brick[0][0], y3, old_brick[0][2]], [old_brick[0][0], y4, old_brick[1][2]]])
    return new_old_list_brick


def check_brick_overlay(old_brick, brick):
    intersection_x = (old_brick[0][0] <= brick[1][0] and old_brick[1][0] >= brick[0][0])
    intersection_y = (old_brick[0][1] <= brick[1][1] and old_brick[1][1] >= brick[0][1])
    return intersection_x and intersection_y


def calculate_falling_bricks(list_bricks):
    map_top_layer =[]
    new_list_bricks = copy.deepcopy(list_bricks)
    for bricks in new_list_bricks:
        height_bricks = bricks[1][2] - bricks[0][2]
        list_height_old_bricks = [0]
        new_map_top_layer = []
        for lying_brick in map_top_layer:
            if check_brick_overlay(lying_brick, bricks):
                list_remains = get_new_coordinates_of_the_top_layer(lying_brick, bricks)
                new_map_top_layer.extend(list_remains)
                list_height_old_bricks.append(lying_brick[1][2])

            else:
                new_map_top_layer.append(lying_brick)

        bricks[0][2] = max(list_height_old_bricks)+1
        bricks[1][2] = max(list_height_old_bricks) + 1 + height_bricks
        new_map_top_layer.append(bricks)
        map_top_layer = copy.deepcopy(new_map_top_layer)
    return new_list_bricks


def find_maximum_height(list_bricks):
    max_height = 0
    for i in list_bricks:
        max_height = max([max_height, i[1][2]])
    return max_height


def decompose_into_list_of_heights_top(list_bricks):
    max_height = find_maximum_height(list_bricks)
    list_of_heights = [[] for _ in range(max_height)]
    for bricks in list_bricks:
        list_of_heights[bricks[1][2]-1].append(bricks)
    list_of_heights = [i for i in list_of_heights]

    return list_of_heights


def decompose_into_list_of_heights_bottom(list_bricks):
    max_height = find_maximum_height(list_bricks)
    list_of_heights = [[] for _ in range(max_height)]
    for bricks in list_bricks:
        list_of_heights[bricks[0][2]-1].append(bricks)
    list_of_heights = [i for i in list_of_heights]
    return list_of_heights


def get_set_id_held_bricks(bricks, list_higher_bricks):
    new_set = set()
    for i in range(len(list_higher_bricks)):
        if check_brick_overlay (bricks,list_higher_bricks[i]):
            new_set.add(i)
    return new_set


def calculate_paired_supports(list_of_heights_top,list_of_heights_bottom):
    sum_extra = len(list_of_heights_top[-1])
    for i in range(len(list_of_heights_top)-1):
        # if len(list_of_heights_top[i]) <= 1:
        #     continue
        if len(list_of_heights_bottom[i+1]) == 0:
            sum_extra += len(list_of_heights_top[i])
            continue
        list_set_index_held = []
        for bricks in list_of_heights_top[i]:
            list_set_index_held.append(get_set_id_held_bricks(bricks, list_of_heights_bottom[i+1]))
        for set_higher_bricks in list_set_index_held:
            # if not set_higher_bricks:
            #     sum_extra += 1
            #     continue
            check_list_set_index_held = copy.deepcopy(list_set_index_held)
            check_list_set_index_held.remove(set_higher_bricks)
            can_remove_all = set_higher_bricks - set().union(*check_list_set_index_held)
            if not can_remove_all:
                sum_extra += 1
    return sum_extra


t1 = time.time()
start_map = [parser_map(i) for i in list_txt]
start_map.sort(key=sort_list_coordinates_z)
new_map = calculate_falling_bricks(start_map)
map_list_of_heights_top = decompose_into_list_of_heights_top(new_map)
map_list_of_heights_bottom = decompose_into_list_of_heights_bottom(new_map)
sum_bricks_extra = calculate_paired_supports(map_list_of_heights_top,map_list_of_heights_bottom)
t2 = time.time()
print(f"Решение задания 1: {sum_bricks_extra}")
print(f"время {t2-t1}")


def count_falls(list_of_heights_top, list_of_heights_bottom, bricks):
    sum_falls = 0
    del_set_bricks = set((bricks,))
    upper_floor_top = bricks[1][2]-1
    if upper_floor_top >= len(list_of_heights_top):
        return sum_falls
    for i in range(upper_floor_top,len(list_of_heights_top)):
        for del_bricks in del_set_bricks:
            list_of_heights_top[del_bricks[1][2]-1].remove(del_bricks)

            sum_falls +=1
        hew_del_set_bricks = set()
        if i+1 >= len(list_of_heights_bottom):
            continue
        for bricks_bottom in list_of_heights_bottom[i+1]:
            if not len(get_set_id_held_bricks(bricks_bottom, list_of_heights_top[i])):
                hew_del_set_bricks.add(bricks_bottom)
        del_set_bricks = hew_del_set_bricks
    return sum_falls-1


def get_sum_count_falls(list_of_heights_top, list_of_heights_bottom, list_bricks):
    sum_count_falls = 0
    for bricks in list_bricks:
        new_list_of_heights_top = copy.deepcopy(list_of_heights_top)
        new_list_of_heights_bottom = copy.deepcopy(list_of_heights_bottom)
        sum_falls = count_falls(new_list_of_heights_top, new_list_of_heights_bottom, bricks)

        sum_count_falls += sum_falls

        # max_count_falls = max([max_count_falls, sum_falls])
    # print(del_block)
    return sum_count_falls


t1 = time.time()
new_map = [(tuple(i[0]),tuple(i[1])) for i in new_map]
map_list_of_heights_bottom_tuple = [list((tuple(i[0]),tuple(i[1])) for i in j) for j in map_list_of_heights_bottom]
map_list_of_heights_top_tuple = [list((tuple(i[0]),tuple(i[1])) for i in j) for j in map_list_of_heights_top]
# count_falls(map_list_of_heights_top_tuple, map_list_of_heights_bottom_tuple, ((6, 5, 1), (6, 5, 4)))
sum_block = get_sum_count_falls(map_list_of_heights_top_tuple,map_list_of_heights_bottom_tuple, new_map)
print(sum_block)
t2 = time.time()
print(f"Решение задания 2: {sum_block}")
print(f"время {t2-t1}")





