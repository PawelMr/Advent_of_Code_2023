import copy
import re
with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


def find_block(name_block, list_ful_string):
    if name_block in list_ful_string:
        index_start = list_ful_string.index(name_block) + 1
        if "\n" in list_ful_string[index_start:]:
            index_end = list_ful_string.index("\n", index_start)
        else:
            index_end = len(list_ful_string)
        return list_ful_string[index_start:index_end]
    else:
        raise Exception(f"в списке нет элемента: {name_block}")


def block_txt_in_int(block_list_txt):
    block_list_int = []
    for i in block_list_txt:
        block_list_int.append(disassemble_into_numbers(i))
    return block_list_int


seeds = disassemble_into_numbers(list_txt[0])

seed_to_soil = block_txt_in_int(find_block("seed-to-soil map:\n", list_txt))
soil_to_fertilizer = block_txt_in_int(find_block("soil-to-fertilizer map:\n", list_txt))
fertilizer_to_water = block_txt_in_int(find_block("fertilizer-to-water map:\n", list_txt))
water_to_light = block_txt_in_int(find_block("water-to-light map:\n", list_txt))
light_to_temperature = block_txt_in_int(find_block("light-to-temperature map:\n", list_txt))
temperature_to_humidity = block_txt_in_int(find_block("temperature-to-humidity map:\n", list_txt))
humidity_to_location = block_txt_in_int(find_block("humidity-to-location map:\n", list_txt))
print()


def move_values_to_new_range(list_values, list_map_range):
    list_new_values = []
    for value in list_values:
        new_value = one_values_to_new_values(value, list_map_range)
        list_new_values.append(new_value)
    return list_new_values


def one_values_to_new_values(value, list_map_range):
    new_value = None
    for map_range in list_map_range:
        if map_range[1] <= value <= (map_range[1]+map_range[2]-1):
            new_value = map_range[0] + value - map_range[1]
    if new_value is None:
        new_value = value
    return new_value


seeds_1 = move_values_to_new_range(seeds, seed_to_soil)
seeds_2 = move_values_to_new_range(seeds_1, soil_to_fertilizer)
seeds_3 = move_values_to_new_range(seeds_2, fertilizer_to_water)
seeds_4 = move_values_to_new_range(seeds_3, water_to_light)
seeds_5 = move_values_to_new_range(seeds_4, light_to_temperature)
seeds_6 = move_values_to_new_range(seeds_5, temperature_to_humidity)
seeds_7 = move_values_to_new_range(seeds_6, humidity_to_location)

print(f"Решение задания 1: {min(seeds_7)}")


def move_list_values_to_list_range(list_values):
    new_list_range_values = []
    for i in range(len(list_values)):
        if not (i % 2):
            new_list_range_values.append([list_values[i]])
        else:
            new_list_range_values[i // 2].append(list_values[i-1]+list_values[i]-1)
    new_list_range_values.sort(key=lambda x: x[0])
    return new_list_range_values


def separation_one_range_by_one_map(one_range,one_map):
    end_one_map = (one_map[1] + one_map[2] - 1)
    start_one_map = one_map[1]
    if one_range[0]>= start_one_map and one_range[1] <= end_one_map:
        return False # [one_range]
    if start_one_map <= one_range[0] < end_one_map < one_range[1]:
        return [[one_range[0],end_one_map],[end_one_map+1, one_range[1]]]
    if one_range[0] < start_one_map <= one_range[1] <= end_one_map:
        return [[one_range[0],start_one_map-1],[start_one_map, one_range[1]]]
    if (one_range[0]< start_one_map and one_range[1] < start_one_map) or one_range[0] > end_one_map :
        return False
    if one_range[0] < start_one_map <= end_one_map < one_range[1]:
        return [[one_range[0],start_one_map-1],[start_one_map,end_one_map],[end_one_map+1, one_range[1]]]
    raise Exception(f"не определили диапазон {one_range} по карте {one_map}")


def join_one_range_by_one_map(one_range, previous_range, one_map):
    end_one_map = (one_map[1] + one_map[2] - 1)
    start_one_map = one_map[1]
    if (one_range[0] >= start_one_map and one_range[1] <= end_one_map
            and previous_range[0] >= start_one_map and previous_range[1] <= end_one_map
            and one_range[0] - previous_range[0] == 1):
        return [[previous_range[0], one_range[1]]]
    else:
        return False


def check_fix_list_range_values_by_map(list_range, map_transition):
    new_list_range = copy.deepcopy(list_range)
    new_list_range.sort(key=lambda x: x[0])
    index = 0
    rebut_while = False
    while index < len(new_list_range):
        one_range = new_list_range[index]
        for i in map_transition:
            new_element_list_range = separation_one_range_by_one_map(one_range, i)
            if new_element_list_range:
                new_list_range = new_list_range[0:index] + new_element_list_range + new_list_range[index+1:]
                rebut_while = True
                break
            if index > 0:
                join_range = join_one_range_by_one_map(one_range, new_list_range[index-1], i)
                if join_range:
                    new_list_range = new_list_range[0:index-1] + join_range + new_list_range[index+1:]
                    index -= 1
                    rebut_while = True
                    break
        if rebut_while:
            rebut_while = False
        else:
            index += 1
    return new_list_range


def translate_range_on_the_map(list_range, map_transition):
    new_list_range = []
    for one_range in list_range:
        new_range = move_values_to_new_range(one_range, map_transition)
        new_list_range.append(new_range)
    new_list_range.sort(key=lambda x: x[0])
    return new_list_range


list_range_values = move_list_values_to_list_range(seeds)

list_range_values = check_fix_list_range_values_by_map(list_range_values, seed_to_soil)
list_range_values_1 = translate_range_on_the_map(list_range_values, seed_to_soil)

list_range_values_1 = check_fix_list_range_values_by_map(list_range_values_1, soil_to_fertilizer)
list_range_values_2 = translate_range_on_the_map(list_range_values_1, soil_to_fertilizer)

list_range_values_2 = check_fix_list_range_values_by_map(list_range_values_2, fertilizer_to_water)
list_range_values_3 = translate_range_on_the_map(list_range_values_2, fertilizer_to_water)

list_range_values_3 = check_fix_list_range_values_by_map(list_range_values_3, water_to_light)
list_range_values_4 = translate_range_on_the_map(list_range_values_3, water_to_light)

list_range_values_4 = check_fix_list_range_values_by_map(list_range_values_4, light_to_temperature)
list_range_values_5 = translate_range_on_the_map(list_range_values_4, light_to_temperature)

list_range_values_5 = check_fix_list_range_values_by_map(list_range_values_5, temperature_to_humidity)
list_range_values_6 = translate_range_on_the_map(list_range_values_5, temperature_to_humidity)

list_range_values_6 = check_fix_list_range_values_by_map(list_range_values_6, humidity_to_location)
list_range_values_7 = translate_range_on_the_map(list_range_values_6, humidity_to_location)

print(f"Решение задания 2: {list_range_values_7[0][0]}")
