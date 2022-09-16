from cgi import test

# from msilib.schema import Error
import os
import json
import time


def store_data_json(id, json_data):
    dir = "database/%s.json" % id
    with open(dir, "w") as file_object:
        json.dump(json_data, file_object, indent=4)
        file_object.flush()
        os.fsync(file_object)
        file_object.close()


def read_database(id):
    datadb = open("database/%s.json" % id)
    datadb.flush()
    data = json.load(datadb)
    datadb.close()
    # data_value = data[address]

    return data


def test(t, r, s, v0, v1, v2, c0, c1, c2, c3):

    try:
        data_tegangan = read_database("voltage")
        data_tegangan["voltage"] = t
        store_data_json("voltage", data_tegangan)
    except Exception as e:
        print("tegangan error :", e)

    try:
        data_kecepatan = read_database("speed")
        data_kecepatan["speed"] = r
        store_data_json("speed", data_kecepatan)
    except Exception as e:
        print("tegangan error :", e)

    try:
        data_suhu = read_database("temperature")
        data_suhu["temperature"] = s
        store_data_json("temperature", data_suhu)
    except Exception as e:
        print("tegangan error :", e)

    data_vinfo = read_database("vehicle_info")
    data_vinfo["mode"] = v0
    data_vinfo["turn_signal"][0] = v1
    data_vinfo["turn_signal"][1] = v2
    store_data_json("vehicle_info", data_vinfo)

    data_connection = read_database("connection")
    data_connection["wifi"]["id"] = c0
    data_connection["wifi"]["pass"] = c1
    data_connection["restart"] = c2
    data_connection["screen"] = c3
    store_data_json("connection", data_connection)


def test_low(delay):
    time.sleep(delay)
    test("0.00", "0.00", "0.0", "n", False, False, "", "", False, "Main")
    time.sleep(2)

    data_odometer = read_database("odometer")
    data_odometer["total_km"] = "0.000"
    store_data_json("odometer", data_odometer)


def test_high(delay):
    time.sleep(delay)
    test("80.00", "70.00", "30.0", "e", True, False, "", "", False, "Main")

    time.sleep(2)

    test("74.00", "40.00", "50.0", "s", False, True, "", "", False, "Main")
    # if speed == "40.00":
    #     print(f"speed component ... {bcolors.OKGREEN}SUCCESS{bcolors.OKGREEN}")
    # else:
    #     print(f"speed component ... {bcolors.FAIL}FAILED{bcolors.FAIL}")


def test_channel(delay):
    time.sleep(delay)
    data_connection = read_database("connection")
    data_connection["screen"] = "Map"
    store_data_json("connection", data_connection)
    time.sleep(delay)
    data_connection = read_database("connection")
    data_connection["screen"] = "About"
    store_data_json("connection", data_connection)


def status_high(file, name, value):
    opdata = open("database/" + file + ".json")
    data = json.load(opdata)
    id_data = data[name]

    if id_data == value:
        print(name + " component ... " + success())
    else:
        # print(f"{bcolors.FAIL}" + name + f" component ... FAILED{bcolors.FAIL}")
        print(name + " component ... " + failed())


def failed():
    return f"{bcolors.FAIL}FAILED{bcolors.DEFAULT}"


def success():
    return f"{bcolors.OKGREEN}SUCCESS{bcolors.DEFAULT}"


def main():
    # time.sleep(2)
    test_low(0)
    test_high(2)
    status_high("speed", "speed", "40.00")
    status_high("temperature", "temperature", "50.0")
    test_channel(5)
    status_high("odometer", "total_km", "0.131")
    test_low(3)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    DEFAULT = "\033[37m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


if __name__ == "__main__":
    main()
