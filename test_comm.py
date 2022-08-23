# import json_stream
import fnmatch
from subprocess import Popen, PIPE, STDOUT
# from kivy.clock import Clock


def hextodec(hex):
    c = count = i = 0
    length = len(hex) - 1
    while length >= 0:
        if hex[length] >= '0' and hex[length] <= '9':
            rem = int(hex[length])
        elif hex[length] >= 'A' and hex[length] <= 'F':
            rem = ord(hex[length]) - 55
        elif hex[length] >= 'a' and hex[length] <= 'f':
            rem = ord(hex[length]) - 87
        else:
            c = 1
            break
        count = count + (rem * (16 ** i))
        length = length - 1
        i = i+1
    return count


def value_bytes(list_bytes, start, length):
    i = 0
    # start_before = 0
    while i < length:
        if length > 1:
            value = list_bytes[start]+list_bytes[start+i]
            # start_before = start + 1
        else:
            value = list_bytes[start]
        i += 1
    data = hextodec(value)
    return data


def main():
    data_dec = "c0 14 0d 59 42 02 14 00 0f 01 00 00 00 00 02 b8 5d 4b 22 d6 80 03 01 0d"
    # data_dec = line.decode('utf-8')
    # print(data_dec)
    list_data = data_dec.split()
    print(list_data)
    battery_voltage_value = value_bytes(list_data, 5, 2)/10
    battery_current_value = value_bytes(list_data, 7, 2)/10
    controller_vault_value = hex(value_bytes(list_data, 10, 4))
    motor_speed_value = value_bytes(list_data, 14, 2)
    controller_temp_value = value_bytes(list_data, 16, 1) - 50
    external_temp_value = value_bytes(list_data, 17, 1) - 50

    controller_status = value_bytes(list_data, 21, 1)
    controller_status_list = ["IDLE", "INIT", "START",
                              "RUN", "STOP", "BROKE", "WAIT", "FAULT"]
    controller_status_value = controller_status_list[controller_status]

    # battery_voltage_bytes = list_data[5] + list_data[6]
    # battery_voltage_value = int(battery_voltage_bytes, 16)/10
    print(battery_voltage_value)
    print(battery_current_value)
    print(motor_speed_value)
    print(controller_temp_value)
    print(external_temp_value)
    print(controller_status_value)
    print(controller_vault_value)


if __name__ == '__main__':
    main()
