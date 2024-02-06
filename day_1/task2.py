import re

with open("input2.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()

print()
old_list_txt = list_txt

# for txt in list_txt:
#     txt = re.sub(r"[^\d\.]", r'', txt).strip()
#     print()
# list_txt = [txt.replace() for txt in list_txt]

def multiple_replace(target_str):
    replace_values = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    new_target_list = []
    for index in range(len(target_str)):
        if target_str[index].isdigit():
            new_target_list.append(target_str[index])
        else:
            for key, value in replace_values.items():
                if target_str[index:].startswith(key):
                    new_target_list.append(str(value))
    new_target_str = "".join(new_target_list)
    return new_target_str

    # while True:
    #     dict_in_txt = {}
    #     for value in replace_values:
    #         if target_str.count(value) >= 1:
    #             start = target_str.find(value)
    #             dict_in_txt.update({start: value})
    #     if not dict_in_txt:
    #         break
    #     list_index = list(dict_in_txt.keys())
    #     target_str = (
    #         target_str.replace(dict_in_txt[min(list_index)],
    #                            str(replace_values.index(dict_in_txt[min(list_index)]) + 1), 1))
    # # if dict_in_txt:
    #     list_index = list(dict_in_txt.keys())
    #     target_str = (
    #         target_str.replace(dict_in_txt[min(list_index)], str(replace_values.index(dict_in_txt[min(list_index)]) + 1)))
    #     target_str = (
    #         target_str.replace(dict_in_txt[max(list_index)], str(replace_values.index(dict_in_txt[max(list_index)]) + 1)))


        # меняем все target_str на подставляемое
        # target_str = target_str.replace(value, str(index+1))
    # return target_str


list_txt = [multiple_replace(txt) for txt in list_txt]
# list_txt = [re.sub(r"[^\d\.]", r'', txt).strip() for txt in list_txt]
print()

list_int = [int(txt[0]+txt[-1]) for txt in list_txt]
print()
value = sum(list_int)
print(f"Решение задания 2: {value}")
