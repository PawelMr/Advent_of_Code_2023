import copy
import re
import collections
import time
import math
import random

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def disassemble_circuit(list_str):
    new_dict = {}
    for string in list_str:
        string = string.replace("\n","")
        list_one = string.split(": ")
        key = list_one[0]
        value = list_one[1].split(" ")
        new_dict.update({key: set(value)})
    return new_dict


def get_complete_scheme(old_scheme):
    new_scheme = copy.deepcopy(old_scheme)
    for key, value in old_scheme.items():
        if not new_scheme.get(key):
            new_scheme.update({key: value})
        else:
            new_scheme[key].update(value)
        for i in value:
            if not new_scheme.get(i):
                new_scheme.update({i: {key}})
            else:
                if key not in new_scheme[i]:
                    new_scheme[i].update({key})
    return new_scheme


def get_shortest_way(step_start, step_finish, dict_fork, list_exclude=[]):
    turn_map = [(step_start, True)]
    visited_points = []
    number_paths = len(dict_fork)
    paths = None
    while turn_map:
        step, not_dell = turn_map.pop()
        if not_dell is None:
            visited_points.remove(step)
            continue
        if step == step_finish:
            if number_paths > len(visited_points):
                number_paths = len(visited_points)
                paths = copy.deepcopy(visited_points)
            continue
        if step in visited_points:
            continue
        visited_points.append(step)
        turn_map.append((step, None))
        for new_step in dict_fork[step]:
            if (step, new_step) in list_exclude:
                continue
            turn_map.append((new_step, True))
    if paths:
        paths.append(step_finish)
    return paths


# алгоритм поиска в глубину
def get_path(start, end, graph, list_exclude=()):
    """
    returns the shortest path between start and end
    The solution doesn't NEED the shortest path (in fact it might be better random) but each cycle is quicker if we do
    """
    prev = {start: start}
    nodes = [start]
    seen = {start}
    while nodes:
        new_nodes = []
        for node in nodes:
            for neighbour in graph[node]:
                if neighbour in seen:
                    continue
                if (node, neighbour) in list_exclude:
                    continue
                seen.add(neighbour)
                prev[neighbour] = node
                new_nodes.append(neighbour)
        nodes = new_nodes

    if prev.get(end) is None:
        return None

    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev[node]
    path.append(start)
    return path[::-1]


def dell_three_ways(step_start, step_finish,dict_fork):
    exclude_list = []
    for nom_paths in range(3):
        paths = get_path(step_start, step_finish, dict_fork, exclude_list)
        for i in range(0, len(paths)-1):
            exclude_list.append((paths[i], paths[i+1]))
            # dict_fork[paths[i]].remove(paths[i+1])
            # dict_fork[paths[i+1]].remove(paths[i])
    return exclude_list


def split_into_two_groups(dict_fork):
    list_nodes = [i for i in dict_fork]
    group_1 = [list_nodes[0]]
    group_2 = []
    for ind in range(1, len(list_nodes)):

        exclude_list = dell_three_ways(list_nodes[0], list_nodes[ind], dict_fork)
        fourth_way = get_path(list_nodes[0], list_nodes[ind], dict_fork, exclude_list)

        if fourth_way:
            group_1.append(list_nodes[ind])
        else:
            group_2.append(list_nodes[ind])
    return group_1, group_2


def find_random_path(dict_fork,count_paths):
    sum_collection_path = collections.Counter()
    for _ in range(count_paths):  # higher range means more likely to be correct
        start, finish = random.sample(list(dict_fork.keys()), 2)
        if finish in dict_fork[start] or start == finish:
            continue
        paths = get_path(start, finish, dict_fork, ())
        path_crossings = []
        for i in range(0, len(paths)-1):
            crossings = [paths[i], paths[i+1]]
            crossings.sort()
            path_crossings.append(tuple(crossings))
        sum_collection_path += collections.Counter(path_crossings)
    return sum_collection_path

t1 = time.time()
circuit_original = disassemble_circuit(list_txt)
complete_scheme = get_complete_scheme(circuit_original)

# get_path("cmg", "ntq", complete_scheme)
#
#
# sum_collection = find_random_path(complete_scheme,200)
# list_key_sum_collection = sorted(list(sum_collection.keys()), key=lambda x: sum_collection[x], reverse=True)
global_group_1, global_group_2 = split_into_two_groups(complete_scheme)
t2 = time.time()
print(f"Решение задания 2: {len(global_group_1) * len(global_group_2)}")
print(f"время {t2-t1}")




