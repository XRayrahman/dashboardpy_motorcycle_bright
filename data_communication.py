# from curses import baudrate
# from msilib.schema import Error
import os
import sys
import serial
import time
import json
# import json_stream
import fnmatch

# from main import reset


def arduino_ports(preferred_list=['*']):
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


def store_data_arduino(id, value):
    try:
        data = read_database(id)
        data[id] = value
        update_database(id, data)
    except Exception as e:
        print('%s error :' % id, str(e))


def data_arduino(ser):
    onWhile = True
    while onWhile == True:
        try:
            # try:
            line = ser.readline()
            data_dec = line.decode('utf-8')
            data = json.loads(data_dec)
            # except:
            #     print("data can't be read, flash the arduino again")

            if len(str(data)) != 0:
                voltage = data['t']
                store_data_arduino("voltage", voltage)

                speed = data['r']
                store_data_arduino("speed", speed)

                temperature = data['s']
                store_data_arduino("temperature", temperature)

                try:
                    vehicle_info = read_database("vehicle_info")
                    vehicle_info["mode"] = data['mode']
                    vehicle_info["turn_signal"][0] = data['turn'][0]
                    vehicle_info["turn_signal"][1] = data['turn'][1]
                    update_database("vehicle_info", vehicle_info)
                except Exception as e:
                    print('vehicle_info error :', str(e))
                    # for now
                    pass

                try:
                    statusEstimation = data['isRun']
                    if statusEstimation == True:
                        # ganti layar
                        try:
                            screen_change = data['screen']
                        except:
                            screen_change = "Main"

                        # koneksi
                        try:
                            bluetooth_wifi_id = data['wifi_id']
                            bluetooth_wifi_pass = data['wifi_pass']
                            restart_wifi = data['restart']
                        except:
                            print('wifi not valid')
                            bluetooth_wifi_id = ""
                            bluetooth_wifi_pass = ""
                            restart_wifi = False

                        connection = {
                            "wifi": {
                                "id": bluetooth_wifi_id,
                                "pass": bluetooth_wifi_pass
                            },
                            "restart": restart_wifi,
                            "screen": screen_change
                        }

                        update_database("connection", connection)

                        # estimasi
                        try:
                            ori_latitude = data['o_lat']
                            ori_longitude = data['o_lng']
                            # isConnected = True
                        except:
                            ori_latitude = ""
                            ori_longitude = ""

                        try:
                            dest_latitude = data['d_lat']
                            dest_longitude = data['d_lng']
                        except:
                            dest_latitude = ""
                            dest_longitude = ""

                        estimation = {
                            "address": {
                                "origin": {
                                    "latitude": ori_latitude,
                                    "longitude": ori_longitude
                                },
                                "destination": {
                                    "latitude": dest_latitude,
                                    "longitude": dest_longitude
                                }
                            }
                        }

                        update_database("estimation", estimation)
                except:
                    statusEstimation = False
            else:
                print("Time out! Exit.\n")
                pass
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
        available_ports = arduino_ports()
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
        data_arduino(port)
        return True


def main():
    # reset()
    onLoop = True
    i = 1
    baudrate = 115200
    while True:
        while onLoop == True:
            print("try "+str(i))
            available_ports = arduino_ports()
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
            data_arduino(port)


    # print(format(float(data), ".2f"))
if __name__ == '__main__':
    main()
