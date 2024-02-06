import re
with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def find_number_cart(text):
    pattern = f'(\\d+)'
    number = re.search(pattern, text).group()
    return int(number)

def disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


dict_cart = {}
dict_cart_prize_numbers = {}
dict_cart_points = {}
dict_dict_cart_cart = {}
summ_points = 0
for txt in list_txt:
    list_cart = txt.split(":")
    number_cart = find_number_cart(list_cart[0])
    list_card_values = list_cart[1].split("|")
    winning_numbers = disassemble_into_numbers(list_card_values[0])
    available_numbers = disassemble_into_numbers(list_card_values[1])
    dict_cart.update({number_cart: (winning_numbers, available_numbers)})
    prize_numbers_list = []
    for i in available_numbers:
        if i in winning_numbers:
            prize_numbers_list.append(i)
    dict_cart_prize_numbers.update({number_cart: prize_numbers_list})
    if len(prize_numbers_list) == 0:
        points = 0
    if len(prize_numbers_list) >= 1:
        points = 2 ** (len(prize_numbers_list) - 1)
    dict_cart_points.update({number_cart: points})
    dict_dict_cart_cart.update({number_cart: {"кол-во карт": 1, "кол-во выиг. ном.": len(prize_numbers_list)}})
    summ_points += points

for index_game in range(1,len(dict_dict_cart_cart)+1):
    for i in range(1, dict_dict_cart_cart[index_game]["кол-во выиг. ном."] + 1):
        if dict_dict_cart_cart.get(index_game+i):
            dict_dict_cart_cart[index_game+i]["кол-во карт"] += dict_dict_cart_cart[index_game]["кол-во карт"]
print(f"Решение задания 1: {summ_points}")

sum_cart = 0
for cart in dict_dict_cart_cart:
    sum_cart += dict_dict_cart_cart[cart]['кол-во карт']

print(f"Решение задания 2: {sum_cart}")
# print(f"Решение задания 1: {sum_list_real_game}")
#
#
#
# print(f"Решение задания 2: {sum_pover}")
