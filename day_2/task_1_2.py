import re
with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def number_cubes(text, colour):
    pattern = f'(\\d+) {colour}'
    number_list = re.findall(pattern, text)
    number_list = [int(i) for i in number_list]
    number = max(number_list) if number_list else 0
    return number


def number_game(text):
    pattern = f'(\\d+)'
    number = re.search(pattern, text).group()
    return int(number)


dict_game = {}
for txt in list_txt:
    list_game = txt.split(":")
    dict_game.update({number_game(list_game[0]): list_game[1]})

dict_game_max_cubes = {}
for key, value in dict_game.items():
    dict_game_max_cubes.update({key: {"blue": number_cubes(value, "blue"),
                                      "green": number_cubes(value, "green"),
                                      "red": number_cubes(value, "red"),}})

list_real_game = []
for key, value in dict_game_max_cubes.items():
    if value['blue'] <= 14 and value['green'] <= 13 and value['red'] <= 12:
        list_real_game.append(key)

sum_list_real_game = sum(list_real_game)
print(f"Решение задания 1: {sum_list_real_game}")

sum_pover = 0
for key, value in dict_game_max_cubes.items():
    sum_pover += value['blue'] * value['green'] * value['red']

print(f"Решение задания 2: {sum_pover}")
