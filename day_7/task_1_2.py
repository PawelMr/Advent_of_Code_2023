import copy
import re
import collections
import time

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()

priority_cards = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "J": 3,
    "T": 4,
    "9": 5,
    "8": 6,
    "7": 7,
    "6": 8,
    "5": 9,
    "4": 10,
    "3": 11,
    "2": 12
}

priority_2_cards = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "T": 3,
    "9": 4,
    "8": 5,
    "7": 6,
    "6": 7,
    "5": 8,
    "4": 9,
    "3": 10,
    "2": 11,
    "J": 12,
}


def sort_by_priority_cards(cards):
    return priority_cards[cards]


def sort_by_priority_2_cards(cards):
    return priority_2_cards[cards]


sort_list_cart = lambda x: (sort_by_priority_cards(x[0]),
                            sort_by_priority_cards(x[1]),
                            sort_by_priority_cards(x[2]),
                            sort_by_priority_cards(x[3]),
                            sort_by_priority_cards(x[4]))
sort_list_cart_and_bet = lambda x: sort_list_cart(x[0])


sort_2_list_cart = lambda x: (sort_by_priority_2_cards(x[0]),
                            sort_by_priority_2_cards(x[1]),
                            sort_by_priority_2_cards(x[2]),
                            sort_by_priority_2_cards(x[3]),
                            sort_by_priority_2_cards(x[4]))
sort_2_list_cart_and_bet = lambda x: sort_2_list_cart(x[0])

# a.sort(key=sort_list_cart_and_bet)


def disassemble_into_numbers(string):
    pattern = r'(\d+)'
    number_txt_list = re.findall(pattern, string)
    number_list = [int(i) for i in number_txt_list]
    return number_list


def get_list_collection_values(str_cart):
    list_cart = list(str_cart)
    collections_cart_values = list(collections.Counter(list_cart).values())
    collections_cart_values.sort(reverse=True)
    return collections_cart_values


def get_list_collection_values_rule_two(str_cart):
    number_j = str_cart.count('J')
    short_str_cart = str_cart.replace("J", "")
    list_cart = list(short_str_cart)
    collections_cart_values = list(collections.Counter(list_cart).values())
    collections_cart_values.sort(reverse=True)
    if collections_cart_values:
        collections_cart_values[0] = collections_cart_values[0]+number_j
    else:
        collections_cart_values = [5]
    return collections_cart_values


def distribute_by_combinations(list_cart_and_bet_for_distribute, rule_two=False):
    dict_combinations = {
        "Пятерка": [],
        "Каре": [],
        "Фулл-хаус": [],
        "Тройка": [],
        "Две пары": [],
        "Одна пара": [],
        "High card": [],
    }
    for hand_cards in list_cart_and_bet_for_distribute:
        if rule_two:
            combinations_cards = get_list_collection_values_rule_two(hand_cards[0])
        else:
            combinations_cards = get_list_collection_values(hand_cards[0])
        if combinations_cards == [5]:
            dict_combinations["Пятерка"].append(hand_cards)
        elif combinations_cards == [4, 1]:
            dict_combinations["Каре"].append(hand_cards)
        elif combinations_cards == [3, 2]:
            dict_combinations["Фулл-хаус"].append(hand_cards)
        elif combinations_cards == [3, 1, 1]:
            dict_combinations["Тройка"].append(hand_cards)
        elif combinations_cards == [2, 2, 1]:
            dict_combinations["Две пары"].append(hand_cards)
        elif combinations_cards == [2, 1, 1, 1]:
            dict_combinations["Одна пара"].append(hand_cards)
        elif combinations_cards == [1, 1, 1, 1, 1]:
            dict_combinations["High card"].append(hand_cards)
        else:
            raise Exception(f"комбинация нормально не определена {hand_cards}")
    return dict_combinations


def sort_dict_combinations_cards(dict_combinations):
    for key, values in dict_combinations.items():
        values.sort(key=sort_list_cart_and_bet)


def sort_dict_combinations_cards_rule_two(dict_combinations):
    for key, values in dict_combinations.items():
        values.sort(key=sort_2_list_cart_and_bet)


def get_list_priority_combinations(dict_combinations):
    list_priority_combinations = []
    list_combinations = ["Пятерка", "Каре", "Фулл-хаус", "Тройка", "Две пары", "Одна пара", "High card"]
    for i in list_combinations:
        if dict_combinations[i]:
            list_priority_combinations.extend(dict_combinations[i])
    return list_priority_combinations


t1 = time.time()
list_cart_and_bet = [i.split(" ") for i in list_txt]

list_cart_and_bet = [[i[0], disassemble_into_numbers(i[1])[0]] for i in list_cart_and_bet]

dict_combinations_cards = distribute_by_combinations(list_cart_and_bet)

sort_dict_combinations_cards(dict_combinations_cards)

list_cart_and_bet_sort_combinations = get_list_priority_combinations(dict_combinations_cards)
list_cart_and_bet_sort_combinations.reverse()

summ_winning = 0

for index, value in enumerate(list_cart_and_bet_sort_combinations):
    summ_winning += value[1] * (index + 1)
t2 = time.time()
print(f"Решение задания 1: {summ_winning}")
print(f"время {t2-t1}")

t1 = time.time()
dict_combinations_cards_rule_two = distribute_by_combinations(list_cart_and_bet,rule_two=True)

sort_dict_combinations_cards_rule_two(dict_combinations_cards_rule_two)

list_cart_and_bet_sort_combinations_rule_two = get_list_priority_combinations(dict_combinations_cards_rule_two)

list_cart_and_bet_sort_combinations_rule_two.reverse()

summ_winning_rule_two = 0

for index, value in enumerate(list_cart_and_bet_sort_combinations_rule_two):
    summ_winning_rule_two += value[1] * (index + 1)

t2 = time.time()
print(f"Решение задания 2: {summ_winning_rule_two}")
print(f"время {t2-t1}")