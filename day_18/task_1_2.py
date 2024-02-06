import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def parser_plan(str_element_map):
    str_element_map = str_element_map.replace("\n", "")
    element_map = str_element_map.split(" ")
    element_map[1] = int(element_map[1])
    return tuple(element_map)


def parser_map(str_element_map):
    str_element_map = str_element_map.replace("\n", "").replace("#", "").replace(")", "").replace("(", "")
    return str_element_map


def find_direction(num_direction):
    dict_direction = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U"
    }
    return dict_direction[num_direction]


def determine_direction(string_direction):
    dict_direction = {
        "R":(1, 1),
        "L":(-1, 1),
        "D":(1, 0),
        "U":(-1, 0)
    }
    direction_sign, index_coordinates = dict_direction[string_direction]
    return direction_sign, index_coordinates


def get_min_length_height(list_point_perimeter):
    min_y, min_x = (0,0)
    for point in list_point_perimeter:
        if point[0] < min_y:
            min_y = point[0]
        if point[1] < min_x:
            min_x = point[1]
    return min_y, min_x


def create_list_of_contour_points(map_plan):
    new_list_point_contour = [[0, 0]]
    for step_plan in map_plan:
        direction_sign, index_coordinates = determine_direction(step_plan[0])
        coordinates_step = [0,0]
        coordinates_step[index_coordinates] = direction_sign
        for step_excovator in range(step_plan[1]):
            latest_point = new_list_point_contour[-1]
            new_list_point_contour.append([latest_point[0]+coordinates_step[0],
                                           latest_point[1]+coordinates_step[1]])
    if new_list_point_contour[0] == new_list_point_contour[-1]:
        new_list_point_contour = new_list_point_contour[:-1]
    min_y, min_x = get_min_length_height(new_list_point_contour)
    update_y = 0 - min_y
    update_x = 0 - min_x
    new_list_point_contour = [(i[0]+update_y, i[1]+update_x) for i in new_list_point_contour]
    return new_list_point_contour


def get_max_length_height(list_point_perimeter):
    max_y, max_x = (0,0)
    for point in list_point_perimeter:
        if point[0] > max_y:
            max_y = point[0]
        if point[1] > max_x:
            max_x = point[1]
    return max_y, max_x


def check_intersection(value_up, value_down, old_inside, flag_point_inside):
    if value_up:
        old_inside = old_inside - 1
    if value_down:
        old_inside = old_inside + 1
    if (value_up or value_down) and old_inside == 0:
        flag_point_inside = not flag_point_inside
    if not -1 <= old_inside <= 1:
        old_inside = 0
    return old_inside, flag_point_inside


def calculate_area(list_point_perimeter):
    max_y, max_x = get_max_length_height(list_point_perimeter)
    new_list_point_inside = []
    for i in range(1, max_y):
        flag_point_inside = False
        old_inside = 0
        for j in range(max_x + 1):
            value_up = True if (i - 1,j) in list_point_perimeter else False
            value_down = True if (i + 1, j) in list_point_perimeter else False
            if (i, j) in list_point_perimeter:
                old_inside, flag_point_inside = check_intersection(value_up,value_down, old_inside, flag_point_inside)
            if flag_point_inside and (i, j) not in list_point_perimeter:
                new_list_point_inside.append((i, j))
    return new_list_point_inside


def build_map(list_contour,list_inside):
    max_y, max_x = get_max_length_height(list_contour)
    matrix = []
    for i in range(max_y+1):
        matrix.append([])
        for j in range(max_x + 1):
            if (i,j) in list_contour:
                meaning = "#"
            elif (i,j) in list_inside:
                meaning = "*"
            else:
                meaning = "."
            matrix[i].append(meaning)
    return matrix

t1 = time.time()
full_map = tuple(parser_plan(i)for i in list_txt)
list_point_contour = create_list_of_contour_points(full_map)
list_point_inside = calculate_area(list_point_contour)
sum_point = len(list_point_inside)+len(list_point_contour)
t2 = time.time()
ful_matrix = build_map(list_point_contour, list_point_inside)
for i in ful_matrix:
    print(i)
print(f"Решение задания 1: {sum_point}")
print(f"время {t2-t1}")


def find_vertices_of_perimeter(map_plan):
    new_list_point_vertices = [[0, 0]]
    for step_plan in map_plan:
        direction_sign, index_coordinates = determine_direction(step_plan[0])
        coordinates_step = [0, 0]
        coordinates_step[index_coordinates] = direction_sign * step_plan[1]

        latest_point = new_list_point_vertices[-1]
        new_list_point_vertices.append([latest_point[0] + coordinates_step[0],
                                       latest_point[1] + coordinates_step[1]])

    if new_list_point_vertices[0] == new_list_point_vertices[-1]:
        new_list_point_vertices = new_list_point_vertices[:-1]
    min_y, min_x = get_min_length_height(new_list_point_vertices)
    update_y = 0 - min_y
    update_x = 0 - min_x
    new_list_point_vertices = [(i[0] + update_y, i[1] + update_x) for i in new_list_point_vertices]
    return new_list_point_vertices


def find_area_using_gauss_algorithm(list_vertices):
    area = 0
    for i in range(len(list_vertices)):
        y1, x1 = list_vertices[i]
        y2, x2 = list_vertices[(i + 1) % len(list_vertices)]
        area += (y1 * x2 - y2 * x1)

    area = abs(area) / 2
    return area


t1 = time.time()
full_map_2 = tuple(parser_plan(i)for i in list_txt)
map_2 = tuple(parser_map(i[2]) for i in full_map_2)
map_2 = tuple((find_direction(i[-1]), int(i[:-1], 16)) for i in map_2)
list_point_vertices = find_vertices_of_perimeter(map_2)
list_point_vertices = [(i[0],i[1]+1) for i in list_point_vertices]
max_y_vertices = get_max_length_height(list_point_vertices)[0] + 1
sum_point_2 = int(find_area_using_gauss_algorithm(list_point_vertices) +
               sum(tuple(i[1] for i in map_2 if i[0] in 'D')) + sum(tuple(i[1] for i in map_2 if i[0] in 'L'))+1)

t2 = time.time()

print(f"Решение задания 2: {sum_point_2}")
print(f"время {t2-t1}")






