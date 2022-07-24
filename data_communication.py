from curses import baudrate
# from msilib.schema import Error
import os, sys
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
                #ret.append(SerialPort(d))
                ret.append(d)
    if len(ret) > 0:
        return ret
    # now the rest
    for d in glist:
        #ret.append(SerialPort(d))
        ret.append(d)
    return ret
    
# listen for the input, exit if nothing received in timeout period
def store_data_json(file, json_structure):
    with open(file, 'w') as file_object:  
        json.dump(json_structure, file_object, indent=4)

def store_data_arduino(ser):
    while True:
        try:
            line = ser.readline()
            # print(line)
            data_dec = line.decode('utf-8')
            # print(data_dec)
            # print("----")
            # if (data[0]=='{' ) :
            data=json.loads(data_dec)
            
            # print(data)
            # print(data_dec)
            if len(str(data)) != 0:
                # print(data)
                try:
                    voltage=data['t']
                    data_json_voltage = {
                        "voltage": voltage
                    }

                    path_voltage = "database/voltage.json"
                    store_data_json(path_voltage, data_json_voltage)
                    # voltage_sebelumnya = voltage
                except Exception as e:
                    print('voltage error :',str(e) )
                    # voltage = "0.00"

                try:
                    speed=data['r']
                
                    data_json_speed = {
                        "speed": speed
                    }
                        
                    path_speed = "database/speed.json"
                    store_data_json(path_speed, data_json_speed)
                    # speed_sebelumnya = speed
                except Exception as e:
                    # speed = "0.00"
                    print("speed error : "+str(e))

                try:
                    temperature=data['s']
                    data_json_temperature = {
                        "temperature": temperature
                    }

                    path_temperature = "database/temperature.json"
                    store_data_json(path_temperature, data_json_temperature)
                except Exception as e:
                    print('temperature error :',str(e) )

                try:
                    turn_left= data['turn'][0]
                    turn_right= data['turn'][1]
                    mode_speed = data['mode']

                    data_json_vinfo = {
                        "mode":mode_speed,
                        "turn_signal":{
                            "right":turn_left,
                            "left":turn_right
                        }
                    }
                        
                    path_turn = "database/vehicle_info.json"
                    store_data_json(path_turn, data_json_vinfo)
                except:
                    turn_left=False
                    turn_right=False

                

                try:
                    statusEstimation = data['isRun']
                    if statusEstimation == True:
                        ### ganti layar
                        try:
                            screen_change=data['screen']
                        except:
                            screen_change="Main"

                        ### koneksi
                        try:
                            bluetooth_wifi_id=data['wifi_id']
                            bluetooth_wifi_pass=data['wifi_pass']
                            restart_wifi=data['restart']
                            # isConnected = True
                        except:
                            print('wifi not valid')
                            bluetooth_wifi_id=""
                            bluetooth_wifi_pass=""
                            restart_wifi=False

                            
                        data_json_connection = {
                            "wifi":{
                                "id":bluetooth_wifi_id,
                                "pass":bluetooth_wifi_pass
                            },
                            "restart":restart_wifi,
                            "screen":screen_change
                        }
                        
                        path_connection = "database/connection.json"
                        store_data_json(path_connection, data_json_connection)

                        # print(bluetooth_wifi_id)

                        ### estimasi   
                        try:
                            ori_latitude=data['o_lat']
                            ori_longitude=data['o_lng']
                            # isConnected = True
                        except:
                            # print('origin address not valid')
                            ori_latitude=""
                            ori_longitude=""

                        try:
                            dest_latitude=data['d_lat']
                            dest_longitude=data['d_lng']
                        except:
                            # print('destination address not valid')
                            dest_latitude=""
                            dest_longitude=""

                        data_json_estimation = {
                            "address":{
                                "origin":{
                                    "latitude":ori_latitude,
                                    "longitude":ori_longitude
                                },
                                "destination":{
                                    "latitude":dest_latitude,
                                    "longitude":dest_longitude
                                }
                            }
                        }
                        
                        path_estimation = "database/estimation.json"
                        store_data_json(path_estimation, data_json_estimation)
                except:
                    statusEstimation = False
                    
                # print(statusEstimation)


                    # print(data_json)
                    # file = "database/datastore.json"
                    # with open(file, 'w') as file_object:  #open the file in write mode
                    #     json.dump(data_json, file_object, indent=4)
            else:
                print("Time out! Exit.\n")
                pass

            # else:
            #     pass

        # except Exception as e:
        #     print('data error :',str(e) )
        except:
            pass

def main():
    # reset()
    onLoop = True
    i = 1
    baudrate = 115200
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
        store_data_arduino(port)
    # print(format(float(data), ".2f"))
if __name__ == '__main__':
    main()
   
