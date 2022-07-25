from cgi import test
import json
import time

def store_data_json(file, json_structure):
    with open(file, 'w') as file_object:  
        json.dump(json_structure, file_object, indent=4)

def test_low(delay):
    time.sleep(delay)
    data_json_voltage = {
        "voltage": "0.00"
    }

    path_voltage = "database/voltage.json"
    store_data_json(path_voltage, data_json_voltage)
                
    data_json_speed = {
        "speed": "0.00"
    }
        
    path_speed = "database/speed.json"
    store_data_json(path_speed, data_json_speed)

    data_json_temperature = {
        "temperature": "0.0"
    }

    path_temperature = "database/temperature.json"
    store_data_json(path_temperature, data_json_temperature)

    data_json_vinfo = {
        "mode":"n",
        "turn_signal":[
            False,False
        ]
    }
        
    path_turn = "database/vehicle_info.json"
    store_data_json(path_turn, data_json_vinfo)

                            
    data_json_connection = {
        "wifi":{
            "id":"",
            "pass":""
        },
        "restart":False,
        "screen":"Main"
    }
    
    path_connection = "database/connection.json"
    store_data_json(path_connection, data_json_connection)

    data_json_odometer = {
        "total_km":"0.000"
    }

    path_odometer = "database/odometer.json"
    store_data_json(path_odometer, data_json_odometer)

def test_high(delay):
    time.sleep(delay)
    data_json_voltage = {
        "voltage": "80.00"
    }

    path_voltage = "database/voltage.json"
    store_data_json(path_voltage, data_json_voltage)
                
    data_json_speed = {
        "speed": "40.00"
    }
        
    path_speed = "database/speed.json"
    store_data_json(path_speed, data_json_speed)

    data_json_temperature = {
        "temperature": "30.0"
    }

    path_temperature = "database/temperature.json"
    store_data_json(path_temperature, data_json_temperature)

    data_json_vinfo = {
        "mode":"n",
        "turn_signal":[
            True,False
        ]
    }
        
    path_turn = "database/vehicle_info.json"
    store_data_json(path_turn, data_json_vinfo)
    time.sleep(2)
    data_json_vinfo = {
        "mode":"s",
        "turn_signal":[
            False,True
        ]
    }
        
    path_turn = "database/vehicle_info.json"
    store_data_json(path_turn, data_json_vinfo)

def test_channel(delay):
    time.sleep(delay)
    data_json_connection = {
        "wifi":{
            "id":"",
            "pass":""
        },
        "restart":False,
        "screen":"Map"
    }
    
    path_connection = "database/connection.json"
    store_data_json(path_connection, data_json_connection)
    time.sleep(1)
    data_json_connection = {
        "wifi":{
            "id":"",
            "pass":""
        },
        "restart":False,
        "screen":"About"
    }
    
    path_connection = "database/connection.json"
    store_data_json(path_connection, data_json_connection)

def main():
    # time.sleep(2)
    test_low(0)
    test_high(2)
    test_channel(5)
    test_low(3)


if __name__ == '__main__':
    main()