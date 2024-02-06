import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def convert_string_to_list_numbers(string):
    pattern = r'(-?\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


def find_intersection_xy(point_a, point_b):
    x_a = point_a[0]
    y_a = point_a[1]
    vx_a = point_a[3]
    vy_a = point_a[4]
    x_b = point_b[0]
    y_b = point_b[1]
    vx_b = point_b[3]
    vy_b = point_b[4]
    if vx_a !=0:
        m1 = vy_a / vx_a
    else:
        m1 = 1
    if vx_b !=0:
        m2 = vy_b / vx_b
    else:
        m2 = 1

    if m1 == m2:
        return False

    b1 = y_a - m1 * x_a
    b2 = y_b - m2 * x_b

    x = int((b2 - b1) / (m1 - m2))
    y = int(m1 * x + b1)

    return x, y


def find_time_intersection(point_a, common_point):
    x_a = point_a[0]
    x_c = common_point[0]
    vx_a = point_a[3]
    t = (x_c - x_a)/vx_a
    return t

# def get_point_crossing_time(point_a, point_b):
#     x_a = point_a[0]
#     y_a = point_a[1]
#     vx_a = point_a[3]
#     vy_a = point_a[4]
#     x_b = point_b[0]
#     y_b = point_b[1]
#     vx_b = point_b[3]
#     vy_b = point_b[4]
#     nx = (x_a - x_b) / (vx_b - vx_a)
#     ny = (y_a - y_b) / (vy_b - vy_a)
#     if nx == ny:
#         return nx
#     else:
#         return False


def find_intersection_xz(point_a, point_b):
    x_a = point_a[0]
    z_a = point_a[2]
    vx_a = point_a[3]
    vz_a = point_a[5]
    x_b = point_b[0]
    z_b = point_b[2]
    vx_b = point_b[3]
    vz_b = point_b[5]
    if vx_a !=0:
        m1 = vz_a / vx_a
    else:
        m1 = 1
    if vx_b !=0:
        m2 = vz_b / vx_b
    else:
        m2 = 1

    if m1 == m2:
        return False

    b1 = z_a - m1 * x_a
    b2 = z_b - m2 * x_b

    x = int((b2 - b1) / (m1 - m2))
    z = int(m1 * x + b1)

    return x, z


def make_list_intersections_xy(list_point, limit_xy):
    list_intersections = []
    for index_a in range(len(list_point)-1):
        for index_b in range(index_a+1, len(list_point)):
            point_a = list_point[index_a]
            point_b = list_point[index_b]
            common_point = find_intersection_xy(point_a, point_b)
            if (common_point
                    and limit_xy[0] <= common_point[0] <= limit_xy[1]
                    and limit_xy[0] <= common_point[1] <= limit_xy[1]):
                t_1 = find_time_intersection(point_a, common_point)
                t_2 = find_time_intersection(point_b, common_point)
                list_intersections.append((index_a, index_b, t_1, t_2))
    return list_intersections


t1 = time.time()
start_map = [convert_string_to_list_numbers(i) for i in list_txt]
limit_cub = (200000000000000, 400000000000000)
list_point_inters = make_list_intersections_xy(start_map, limit_cub)
list_future_inters = [i for i in list_point_inters if i[2] >= 0 and i[3] >= 0]
t2 = time.time()
print(f"Решение задания 1: {len(list_future_inters)}")
print(f"время {t2-t1}")


def select_coordinates_xy(list_point, speed_range=(-2000, 2001)):
    new_point_insert = None
    point_inters= vxr= vyr= None
    speed_range_x = speed_range_y = speed_range
    speed_range_x = (-79,-77)
    speed_range_y = (268,270)
    for vxr in range(*speed_range_x):
        for vyr in range(*speed_range_y):
            point_inters = None

            point_a = copy.deepcopy(list_point[0])
            point_a[3] = point_a[3] - vxr
            point_a[4] = point_a[4] - vyr
            for index_b in range(1, len(list_point)):

                point_b =copy.deepcopy( list_point[index_b])
                point_b[3] = point_b[3] - vxr
                point_b[4] = point_b[4] - vyr
                new_point_insert_a_b = find_intersection_xy(point_a, point_b)
                if new_point_insert_a_b:
                    new_point_insert = new_point_insert_a_b
                if point_inters is None:
                    point_inters = new_point_insert
                    continue
                if new_point_insert != point_inters:
                    point_inters = None
                    break

            if point_inters:
                break
        if point_inters:
            break
    return point_inters,vxr,vyr


def select_coordinates_xz(list_point, vxr, speed_range=(-2000, 2001)):
    new_point_insert = None
    point_inters = vzr = None
    speed_range_z = speed_range
    speed_range_z = (70,73)
    for vzr in range(*speed_range_z):
        point_inters = None

        point_a = copy.deepcopy(list_point[0])
        point_a[3] = point_a[3] - vxr
        point_a[5] = point_a[5] - vzr
        for index_b in range(1, len(list_point)):

            point_b =copy.deepcopy( list_point[index_b])
            point_b[3] = point_b[3] - vxr
            point_b[5] = point_b[5] - vzr
            new_point_insert_a_b = find_intersection_xz(point_a, point_b)
            if new_point_insert_a_b:
                new_point_insert = new_point_insert_a_b
            if point_inters is None:
                point_inters = new_point_insert
                continue
            if new_point_insert != point_inters:
                point_inters = None
                break

        if point_inters:
            break
    return point_inters,vxr,vzr


def nok(list_value):
    nok_value = 1
    for i in list_value:
        nok_value = (i * nok_value) // math.gcd(i, nok_value)
    return nok_value


def factor(n):
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        ans.append(n)
    return ans

#  сделано по идеи
#  https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/keq7g67/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# тут сделано круче но не разробрал
# https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/keq47qh/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
#
t1 = time.time()
vx_collections = collections.Counter([i[3] for i in start_map])
vy_collections = collections.Counter([i[4] for i in start_map])
vz_collections = collections.Counter([i[5] for i in start_map])
vx_dict = {}
for key, value in dict(vx_collections).items():
    if value>1:
        list_coordinat = [i[0] for i in start_map if i[3] == key]
        list_coordinat.sort(reverse=True)
        list_coordinat = [list_coordinat[i-1]-list_coordinat[i] for i in range(1, len(list_coordinat))]
        vx_dict.update({key: factor(min(list_coordinat))})
vx_list = [i for j,i in vx_dict.items()]
vy_dict = {}
for key, value in dict(vy_collections).items():
    if value>1:
        list_coordinat = [i[1] for i in start_map if i[4] == key]
        list_coordinat.sort(reverse=True)
        list_coordinat = [list_coordinat[i-1]-list_coordinat[i] for i in range(1, len(list_coordinat))]
        vy_dict.update({key: min(list_coordinat)})
vy_list = [i for j,i in vy_dict.items()]
vz_dict = {}
for key, value in dict(vz_collections).items():
    if value>1:
        list_coordinat = [i[2] for i in start_map if i[5] == key]
        list_coordinat.sort(reverse=True)
        list_coordinat = [list_coordinat[i-1]-list_coordinat[i] for i in range(1, len(list_coordinat))]
        vz_dict.update({key: min(list_coordinat)})
vz_list = [i for j,i in vz_dict.items()]

point_xy = select_coordinates_xy(start_map[:15], speed_range=(-80, 300))
print(point_xy)
point_xz = select_coordinates_xz(start_map[:15],point_xy[1], speed_range=(-80, 300))
print(point_xz)
point_xyz = (point_xy[0][0],point_xy[0][1],point_xz[0][1])
t2 = time.time()
print(f"Решение задания 2: {int(sum(point_xyz))}")
print(f"время {t2-t1}")




