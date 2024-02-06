import copy
import re
import collections
import time
import math

with open("input.txt", mode="r", encoding="utf-8") as test_file:
    list_txt = test_file.readlines()


def translate_map_into_dict(string):
    module, purposes = string.replace("\n", "").split(" -> ")
    if module != 'broadcaster':
        name_module = module[1:]
        type_module = module[0]
    else:
        name_module = module
        type_module = "broad"
    purposes = purposes.replace(" ", "")
    list_purposes = tuple(purposes.split(","))
    return {name_module: (type_module, list_purposes)}


def translate_full_map_into_dict(list_string):
    full_dict_map = {}
    for i in list_string:
        full_dict_map.update(translate_map_into_dict(i))
    return full_dict_map


def create_dictionary_of_states(full_dict_map):
    new_dict_status = {}
    for key, value in  full_dict_map.items():
        if value[0] == "%":
            status = False
        if value[0] == "broad":
            status = None
        if value[0] == "&":
            status = {i: "low" for i, j in full_dict_map.items() if key in j[1]}
        new_dict_status.update({key: status})
    return new_dict_status


def process_trigger_signal(type_signal, status):
    """
    обробатываем сигнал Модули триггера префикс %
    :param type_signal: тип поступившего сигнала
    :param status: статус тригера
    :return:
    """
    if type_signal == "high":
        return status, None
    if type_signal == "low":
        new_signal = "low" if status else "high"
    status = not status
    return status, new_signal


def process_signal_to_connecting_module(type_signal, status, source_of_signal):
    """
    обробатываем сигнал Соединительные модули (префикс &)
    :param type_signal: тип поступившего сигнала
    :param status: статус модуля
    :param source_of_signal: источник сигнала
    :return:
    """
    status[source_of_signal] = type_signal
    common_status_signal_high = all([i == "high" for j, i in status.items()])
    new_signal = "low" if common_status_signal_high else "high"
    return status, new_signal


def process_signal_broad(type_signal):
    new_signal = type_signal
    return new_signal


def execute_one_signal(source, signal, rec, dict_full_map, dict_full_status):
    type_rec = dict_full_map.get(rec, [None, None])[0]
    following_goals = dict_full_map.get(rec, [None, None])[1]
    status_rec = dict_full_status.get(rec, None)
    new_status_rec = None
    if type_rec == '%':
        new_status_rec, new_signal = process_trigger_signal(signal,status_rec)
    elif type_rec == "&":
        new_status_rec, new_signal = process_signal_to_connecting_module(signal, status_rec, source)
    elif type_rec == "broad":
        new_signal = process_signal_broad(signal)
    else:
        new_signal = None
    if not new_status_rec is None:
        dict_full_status[rec] = new_status_rec
    if new_signal:
        list_new_signal = [[rec, new_signal, i] for i in following_goals]
    else:
        list_new_signal = []
    return list_new_signal, dict_full_status


def perform_surge_signal(dict_full_map, dict_full_status):
    list_signal = [["button", "low", "broadcaster"]]
    step = 0
    while True:
        list_new_signal, new_dict_full_status = execute_one_signal(*list_signal[step], dict_full_map, dict_full_status)
        dict_full_status = new_dict_full_status
        list_signal.extend(list_new_signal)
        if step == len(list_signal) - 1:
            break
        else:
            step += 1
    return list_signal, dict_full_status


def repeat_the_wave_several_times(count_iterations, dict_full_map, dict_full_status):
    step = 0
    list_dict_full_status = []
    list_surge = []
    while step < count_iterations:
        list_dict_full_status.append(copy.deepcopy(dict_full_status))
        step += 1
        list_signal, dict_full_status = perform_surge_signal(dict_full_map, dict_full_status)
        # if list_signal in list_surge:
        #     print(f"шаг {step} повторился вызов на  {list_surge.index(list_signal) + 1}")
        # if dict_full_status in list_dict_full_status:
        #     print(f"шаг {step} повторилась настройка на  {list_dict_full_status.index(dict_full_status)}")
        list_surge.append(copy.deepcopy(list_signal))
    return list_surge


def calculate_signals_in_wave(list_signal):
    dict_signal = {"low": 0,
                   "high": 0}
    for i in list_signal:
        dict_signal[i[1]] += 1
    return dict_signal


def calculate_all_signals_in_wave(list_surge):
    dict_all_signal = {"low": 0,
                       "high": 0}
    for list_signal in list_surge:
        dict_signal = calculate_signals_in_wave(list_signal)
        dict_all_signal["low"]+=dict_signal["low"]
        dict_all_signal["high"] += dict_signal["high"]
    return dict_all_signal


# low - низкий
# high - высокий
t1 = time.time()
dict_map = translate_full_map_into_dict(list_txt)
dict_status = create_dictionary_of_states(dict_map)
full_list_surge = repeat_the_wave_several_times(1000, dict_map, dict_status)
ful_dict_signal = calculate_all_signals_in_wave(full_list_surge)
answer = ful_dict_signal["low"]*ful_dict_signal["high"]
t2 = time.time()
print(f"Решение задания 1: {answer}")
print(f"время {t2-t1}")


def repeat_the_wave_several_times_to_modul(modul, dict_full_map, dict_full_status):
    step = 0
    list_dict_full_status = []
    list_surge = []
    step_list_signal_dh = []
    step_list_signal_qd = []
    step_list_signal_dp = []
    step_list_signal_bb = []
    while True:
        # list_dict_full_status.append(copy.deepcopy(dict_full_status))
        step += 1
        list_signal, dict_full_status = perform_surge_signal(dict_full_map, dict_full_status)
        signal_modul = [i for i in list_signal if i[2] == modul and i[1] == "low"]



        list_signal_dh = [i for i in list_signal if i[0] == "dh" and i[1] == "high"]
        if list_signal_dh:
            print([i for i in list_signal if i[0] == "dh"])
            step_list_signal_dh.append(step)
        list_signal_qd = [i for i in list_signal if i[0] == "qd" and i[1] == "high"]
        if list_signal_qd:
            print([i for i in list_signal if i[0] == "qd"])
            step_list_signal_qd.append(step)
        list_signal_dp = [i for i in list_signal if i[0] == "dp" and i[1] == "high"]
        if list_signal_dp:
            print([i for i in list_signal if i[0] == "dp"])
            step_list_signal_dp .append(step)
        list_signal_bb = [i for i in list_signal if i[0] == "bb" and i[1] == "high"]
        if list_signal_bb:
            print([i for i in list_signal if i[0] == "bb"])
            step_list_signal_bb.append(step)
        if len(step_list_signal_dh)>= 2 and len(step_list_signal_qd)>= 2 and len(step_list_signal_dp)>= 2 and len(
                step_list_signal_bb)>= 2:

            return (step_list_signal_dh[1] - step_list_signal_dh[0], step_list_signal_qd[1] - step_list_signal_qd[0],
                    step_list_signal_dp[1] - step_list_signal_dp[0], step_list_signal_bb[1] - step_list_signal_bb[0])
        # if signal_modul:
        #     return step
        # list_surge.append(copy.deepcopy(list_signal))


def get_nok(list_value):
    total_multiple = 1
    for value in list_value:
        total_multiple = (total_multiple * value) // math.gcd(total_multiple, value)
    return total_multiple


# low - низкий
# high - высокий
t1 = time.time()
dict_map = translate_full_map_into_dict(list_txt)
dict_status = create_dictionary_of_states(dict_map)
list_for_nok = repeat_the_wave_several_times_to_modul("rx", dict_map, dict_status)
answer = get_nok(list_for_nok)
t2 = time.time()
print(f"Решение задания 2: {answer}")
print(f"время {t2-t1}")