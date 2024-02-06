import re

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()

print()

# for txt in list_txt:
#     txt = re.sub(r"[^\d\.]", r'', txt).strip()
#     print()

list_txt = [re.sub(r"[^\d\.]", r'', txt).strip() for txt in list_txt]
print()

list_int = [int(txt[0]+txt[-1]) for txt in list_txt]
print()
value = sum(list_int)
print(f"Решение задания 1: {value}")
