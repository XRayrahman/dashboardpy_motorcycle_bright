# from curses import baudrate
# from msilib.schema import Error
import os
import sys
import serial
import time
import json
# import json_stream
import fnmatch
from subprocess import Popen, PIPE, STDOUT
# from kivy.clock import Clock

# from main import reset


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


def serial_ports(preferred_list=['*']):
    '''try to auto-detect serial ports on posix based OS'''
    import glob

    glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    ret = []

    # try preferred ones first
    for d in glist:
        for preferred in preferred_list:
            if fnmatch.fnmatch(d, preferred):
                # ret.append(SerialPort(d))
                ret.append(d)
    if len(ret) > 0:
        return ret
    # now the rest
    for d in glist:
        # ret.append(SerialPort(d))
        ret.append(d)
    return ret

# listen for the input, exit if nothing received in timeout period


def read_database(id):
    datadb = open('database/%s.json' % id)
    datadb.flush()
    data = json.load(datadb)
    datadb.close()
    # data_value = data[address]

    return data


def update_database(id, json_data):
    dir = ('database/%s.json' % id)
    with open(dir, 'w') as file_object:
        json.dump(json_data, file_object, indent=4)
        file_object.flush()
        os.fsync(file_object)
        file_object.close()


def store_data_votol(id, value):
    try:
        data = read_database(id)
        data[id] = value
        update_database(id, data)
    except Exception as e:
        print('%s error :' % id, str(e))


def data_votol(ser, port):
    onWhile = True
    while onWhile == True:
        try:
            # try:
            Popen("./serialdump "+port + " 24", shell=True)
            line = ser.readline()
            data_dec = line.decode('utf-8')
            print(data_dec)
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
            # data = json.loads(data_dec)

        except:
            print("Serial port disconnected")
            onWhile = retry()
            pass


def retry():
    i = 1
    onLoop = True
    baudrate = 115200
    while onLoop == True:
        print("retrying "+str(i))
        available_ports = serial_ports()
        try:
            i += 1
            port = serial.Serial(available_ports[0], baudrate, timeout=3)
            onLoop = False
        except:
            onLoop = True
            pass
        time.sleep(1)

    if onLoop == False:
        print("port(s) detected :")
        print(str(available_ports))
        data_votol(port)
        return True


def main():
    # reset()
    onLoop = True
    i = 1
    baudrate = 115200
    while True:
        while onLoop == True:
            print("try "+str(i))
            available_ports = serial_ports()
            try:
                i += 1
                port = serial.Serial(available_ports[0], baudrate, timeout=3)
                onLoop = False
            except:
                onLoop = True
                pass
            time.sleep(1)
            # if len(str(available_ports)) != 0:
            #     onLoop = False

        if onLoop == False:
            print("port(s) detected :")
            print(str(available_ports))
            data_votol(port, available_ports[0])

    # print(format(float(data), ".2f"))
if __name__ == '__main__':
    main()
