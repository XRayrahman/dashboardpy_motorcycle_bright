from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import StringProperty, NumericProperty
from kivy_gradient import Gradient
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivy.uix.screenmanager import (
    RiseInTransition,
    FadeTransition,
    ScreenManager,
    Screen,
)
from time import strftime
from math import *
from subprocess import Popen, PIPE, STDOUT
from kivy.clock import Clock
from kivy.graphics import Color, Line, SmoothLine
from kivy.graphics.context_instructions import Translate, Scale
from kivy_garden.speedmeter import SpeedMeter

# from kivy_garden.qrcode import QRCodeWidget
from kivy_garden.mapview.utils import clamp
from kivy_garden.mapview import MapView, MapMarker, MapLayer
from kivy_garden.mapview.constants import (
    CACHE_DIR,
    MAX_LATITUDE,
    MAX_LONGITUDE,
    MIN_LATITUDE,
    MIN_LONGITUDE,
)
from kivymd_extensions.akivymd import *
import os
import requests
import joblib
import requests
import json

# Clock.max_iteration = 50

from kivy.config import Config

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.write()

# Window.borderless = True
# Window.size=(800,480)
# Window.fullscreen = True
# Window.maximize()


class Dashboard(MDApp):
    sw_started = False
    sw_seconds = 0
    val = ""
    tuj = ""
    icon = "assets/logo.svg"
    delay_notification = 0
    tegangan_sebelum = 0.00
    screen_manager = ScreenManager()
    jarak_tempuh_total = 0
    kecepatan_sebelum = 0

    # theme-custom
    red = 223 / 255, 91 / 255, 97 / 255, 1
    green = 118 / 255, 209 / 255, 155 / 255, 1
    cyan = 126 / 255, 212 / 255, 240 / 255, 1
    dark_blue = 12 / 255, 49 / 255, 62 / 255, 1
    off = 180 / 255, 180 / 255, 180 / 255, 1
    off_white = 217 / 255, 217 / 255, 217 / 255, 1

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "500"
        self.title = "EVOLION"

        return MyLayout()

    def on_start(self):
        self.root.ids.screen_manager.switch_to(self.root.ids.splashScreen)
        self.subScreen = Clock.schedule_once(self.changeScreen, 12)

        vehicleStatus = self.read_database("vehicle_info")
        vehicleStatus["power"] = "on"
        self.update_database("vehicle_info", vehicleStatus)
        self.root.ids.power_switch.active = True
        self.jarak_sebelumnya = 0
        self.screen_tomap = False

        # schedule_interval(program, interval/waktu dijalankan)
        self.sub1 = Clock.schedule_interval(self.update_status, 5)
        self.sub2 = Clock.schedule_interval(self.update_data_suhu_kecepatan, 0.005)
        self.sub2 = Clock.schedule_interval(self.update_data_soc_tegangan, 3)
        self.sub3 = Clock.schedule_interval(self.odometer, 1)
        self.sub4 = Clock.schedule_interval(self.odometer_submit, 3)
        self.sub5 = Clock.schedule_interval(self.turn_signal, 1)
        self.sub6 = Clock.schedule_interval(self.change_screen_main, 1)
        self.asyncRun = Clock.schedule_once(self.asyncProgram, 10)

    def asyncProgram(self, dt):

        # testing script
        # try:
        #     Popen("python3 tests/data_test.py", shell=True)
        # except:
        #     Popen("python tests/data_test.py", shell=True)

        # arduino communication script
        try:
            Popen("python3 data_communication.py", shell=True)
        except:
            Popen("python data_communication.py", shell=True)

    def changeScreen(self, dt):
        self.root.ids.screen_manager.transition = RiseInTransition()
        self.root.ids.screen_manager.switch_to(self.root.ids.mainScreen)

    def change_screen_main(self, nap):
        if self.sw_started:
            self.sw_seconds += nap

        try:
            dt = open("database/connection.json")
            data_change_screen = json.load(dt)
            change_screen = data_change_screen["screen"]
        except:
            change_screen = "Main"

        if change_screen == "Map":
            self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini2)
            self.root.ids.channels.switch_to(self.root.ids.mapChannel)
            self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
            self.root.wall_path = "assets/grad.png"
            self.root.ids.mode_label.text = "SPEED"
            self.root.ids.power_label.text = "SOC"
            self.root.ids.card_label.text = "NORMAL"
            self.screen_tomap = False

        elif change_screen == "Main":
            if self.screen_tomap == True:
                self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini2)
                self.root.ids.channels.switch_to(self.root.ids.mapChannel)
                self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
                # self.root.ids.walls.source = "assets/grad.png"
                self.root.ids.mode_label.text = "SPEED"
                self.root.ids.power_label.text = "SOC"
                self.root.ids.card_label.text = "NORMAL"
            else:
                self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini1)
                self.root.ids.channels.switch_to(self.root.ids.mainChannel)
                self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop1)
                self.root.ids.mode_label.text = "MODE"
                self.root.ids.power_label.text = "POWER"
                self.root.ids.card_label.text = "APLIKASI"

        elif change_screen == "About":
            self.root.ids.screendget_mini.switch_to(self.root.ids.s_mini1)
            self.root.ids.channels.switch_to(self.root.ids.aboutChannel)
            self.root.ids.menubar_left.switch_to(self.root.ids.menubar_leftTop2)
            # self.root.ids.walls.source = "assets/grad.png"
            self.root.ids.mode_label.text = "SPEED"
            self.root.ids.power_label.text = "SOC"
            self.root.ids.card_label.text = "APLIKASI"
            # self.screen_tomap = False

    def battery_status(self, status):
        currentChannel = self.root.ids.channels.current
        if currentChannel == "mainChannel":
            if status == "low":
                color_bar = self.red
                color_charge = self.off
                color_low = self.red
                color_full = self.off
                color_text = self.red
                Clock.schedule_once(self.blink_battery, 1.5)
            elif status == "high":
                color_bar = self.green
                color_charge = self.off
                color_low = self.off
                color_full = self.green
                color_text = self.off_white
            elif status == "charging":
                color_bar = self.cyan
                color_charge = self.cyan
                color_low = self.off
                color_full = self.off
                color_text = self.off_white
            else:
                color_bar = self.green
                color_charge = self.off
                color_low = self.off
                color_full = self.off
                color_text = self.off_white

            self.root.ids.battery_full.text_color = color_full
            self.root.ids.battery_charging.text_color = color_charge
            self.root.ids.battery_low.text_color = color_low
            self.root.ids.SOC_circular.circle_color = color_bar
            self.root.ids.tegangan_value_text.color = color_text

    def blink_battery(self, *args):
        # icon_color  = self.root.ids.id.text_color
        self.root.ids.battery_low.text_color = self.off

    def blink_temp(self, *args):
        self.root.ids.temp_high.text_color = self.off

    def suhu_animate(self, int_suhu):
        text = self.root.ids.suhu_value_text.text
        space = " "
        value_suhu = text.split(space, 1)[0]
        # int_suhu_sebelum = int(value_suhu)
        # if int_suhu > int_suhu_sebelum:
        #     int_suhu_sebelum += 1
        text_suhu = str(int_suhu) + " °C"
        self.root.ids.suhu_value_text.text = text_suhu
        # elif int_suhu < int_suhu_sebelum:
        #     int_suhu_sebelum -= 1
        #     text_suhu = str(int_suhu_sebelum)+" °C"
        #     self.root.ids.suhu_value_text.text = text_suhu
        if int_suhu >= 60:
            self.root.ids.suhu_value_text.color = self.red
            self.root.ids.temp_high.text_color = self.red
            Clock.schedule_once(self.blink_temp, 1.5)
        elif int_suhu <= 10:
            self.root.ids.suhu_value_text.color = self.cyan
            self.root.ids.temp_high.text_color = self.cyan
        else:
            self.root.ids.suhu_value_text.color = self.off_white
            self.root.ids.temp_high.text_color = self.off_white

    def read_database(self, id):
        datadb = open("database/%s.json" % id)
        datadb.flush()
        data = json.load(datadb)
        datadb.close()
        # data_value = data[address]

        return data

    def update_database(self, id, json_data):
        dir = "database/%s.json" % id
        with open(dir, "w") as file_object:
            json.dump(json_data, file_object, indent=4)
            file_object.flush()
            os.fsync(file_object)
            file_object.close()

    # update data SOC dan tegangan
    def update_data_soc_tegangan(self, nap):
        # tegangan = 0.00
        strtegangan = "0.0"
        if self.sw_started:
            self.sw_seconds += nap
        try:
            data_tegangan = self.read_database("voltage")
            strtegangan = data_tegangan["voltage"]
        except:
            strtegangan = "0.00"

        floattegangan = float(strtegangan)
        if floattegangan > 84.00:
            floattegangan = 84

        inttegangan = format(floattegangan, ".1f")
        tegangan_text = str(inttegangan) + " V"
        # SOC_text = "TEGANGAN : "+ strtegangan +" V"
        self.root.ids.tegangan_value_text.text = tegangan_text

        valtegangan = float(inttegangan)
        if valtegangan >= 84:
            SOC_value = 100
            self.battery_status("high")
        elif valtegangan < 84 and valtegangan >= 76:
            SOC_value = round(100 - ((84 - valtegangan) / 0.8), 1)
            if self.tegangan_sebelum < valtegangan:
                self.battery_status("charging")
            else:
                self.battery_status("high")
        elif valtegangan < 76 and valtegangan >= 72:
            SOC_value = round(90 - ((76 - valtegangan) / 0.067), 1)
            if self.tegangan_sebelum < valtegangan:
                self.battery_status("charging")
            else:
                self.battery_status("neither")
        elif valtegangan < 72 and valtegangan >= 60:
            SOC_value = round(30 - ((72 - valtegangan) / 0.4), 1)
            if self.tegangan_sebelum < valtegangan:
                self.battery_status("charging")
            else:
                self.battery_status("low")
        else:
            SOC_value = round(0, 1)
            # SOC_value = round(30-((60-valtegangan)/2),1)
            self.battery_status("low")

        # SOC_value = round((float(strtegangan)/3)*100, 1)
        self.SOC_value = str(round(SOC_value)) + "%"

        currentChannel = self.root.ids.channels.current
        if currentChannel == "mainChannel":
            self.root.ids.SOC_circular.current_percent = SOC_value
            self.root.ids.SOC_label.text = self.SOC_value
        elif currentChannel == "mapChannel" or "aboutChannel":
            self.root.ids.SOC_ontop.text = self.SOC_value

        if valtegangan >= 84 and self.tegangan_sebelum < 84.00:
            snackbar = CustomSnackbar(
                text="Baterai terisi penuh",
                icon="battery",
                bg_color=self.green,
                snackbar_x="15dp",
                snackbar_y="15dp",
                size_hint_x=(Window.width - (188.5 * 2)) / Window.width,
                # size_hint_x=(
                #     Window.width - (15 * 2)
                # ) / Window.width,
                size_hint_y=0.153,
            )
            snackbar.open()
            self.delay_notification = 0

        # elif valtegangan > 72 and valtegangan < 76 and self.tegangan_sebelum < valtegangan:
        #     snackbar = CustomSnackbar(
        #         text="Baterai Charging",
        #         icon="battery",
        #         bg_color=self.dark_blue,
        #         snackbar_x="15dp",
        #         snackbar_y="15dp",
        #         size_hint_x=(
        #             Window.width - (188.5 * 2)
        #         ) / Window.width,
        #         size_hint_y=0.153
        #     )
        #     snackbar.open()
        #     self.delay_notification = 0
        elif valtegangan < 72 and self.delay_notification == 5:
            # self.popup = MDDialogDef(
            #     title="// NOTIFICATION ALERT //",
            #     text="Sisa Kapasitas baterai dibawah 30% \nCharge kendaraan terlebih dahulu",
            #     radius=[7, 7, 7, 7],
            #     md_bg_color=(215 / 255, 71 / 255, 68 / 255, 1),
            #     size_hint=(0.4,0.1),
            #     # buttons=[
            #     #     MDFlatButton(text="CANCEL"),
            #     #     MDFillRoundFlatButton(text="LOKASI CHARGE TERDEKAT"),
            #     # ],
            # )
            # self.popup.open()
            snackbar = CustomSnackbar(
                icon="battery",
                text="Sisa kapasitas Baterai dibawah 30%",
                bg_color=self.red,
                snackbar_x="15dp",
                snackbar_y="15dp",
                size_hint_x=(Window.width - (188.5 * 2)) / Window.width,
                # size_hint_x=(
                #     Window.width - (15 * 2)
                # ) / Window.width,
                size_hint_y=0.153,
            )
            snackbar.open()
            self.delay_notification = 0
        else:
            self.delay_notification += 1
            if self.delay_notification == 6:
                self.delay_notification = 0
        self.tegangan_sebelum = floattegangan

        # suhu
        try:
            data_suhu = self.read_database("temperature")
            strsuhu = data_suhu["temperature"]
            float_suhu = float(strsuhu)
            intsuhu = int(format(float_suhu, ".0f"))
            if intsuhu >= 100:
                intsuhu = 100
        except:
            intsuhu = 0

        if currentChannel == "mainChannel":
            self.suhu_animate(intsuhu)

    # update data suhu dan kecepatan

    def update_data_suhu_kecepatan(self, nap):
        self.root.ids.progress.value = self.root.ids.progress.value + 0.2
        # tegangan = 0.00
        strtegangan = "0.0"
        if self.sw_started:
            self.sw_seconds += nap

        # kecepatan
        try:
            data_kecepatan = self.read_database("speed")
            self.kecepatan = data_kecepatan["speed"]
        except:
            self.kecepatan = "0.00"

        kecepatan = (float(self.kecepatan) / 6) * 188.4 * 0.036  # kecepatan e-trail
        kecepatan = format(float(kecepatan), ".0f")

        # maksimal kecepatan
        if int(kecepatan) >= 121:
            kecepatan = 120

        speeds = str(kecepatan)

        currentChannel = self.root.ids.channels.current
        if currentChannel == "mainChannel":
            intkec = int(kecepatan)
            kecepatan_sebelum = self.root.ids.speed_bar.value
            if intkec > kecepatan_sebelum:
                kecepatan_sebelum += 1
                self.root.ids.speed_bar.value = kecepatan_sebelum
                self.root.ids.speed_bar_value.text = str(kecepatan_sebelum)
            elif intkec < kecepatan_sebelum:
                kecepatan_sebelum -= 1
                self.root.ids.speed_bar.value = kecepatan_sebelum
                self.root.ids.speed_bar_value.text = str(kecepatan_sebelum)
                # for i in range (kecepatan_sebelum,intkec):
                #     self.root.ids.speed_bar.value = i
                # time.sleep(0.2)
            # self.root.ids.speed_bar_value.text = speeds
        elif currentChannel == "mapChannel" or "aboutChannel":
            speed_value = "%s" % (speeds)
            self.root.ids.speed_ontop.text = speed_value

    def odometer(self, nap):
        # tegangan = 0.00
        # odo = "0.0"
        if self.sw_started:
            self.sw_seconds += nap

        jarak_tempuh = (
            (float(self.kecepatan) / 6) * (188.4 + 37.68) * 0.00001
        )  # odometer e-trail
        self.jarak_tempuh_total_lima = jarak_tempuh + self.jarak_sebelumnya
        self.jarak_sebelumnya = jarak_tempuh

    def odometer_submit(self, nap):
        # tegangan = 0.00
        odo = "0.0"
        if self.sw_started:
            self.sw_seconds += nap

        data_odo = self.read_database("odometer")
        odo = data_odo["total_km"]
        # except Exception as e:
        # print('odo error :',str(e) )

        if len(str(data_odo)) != 0:
            self.jarak_tempuh_total = float(odo)
            # jarak_tempuh = format(float(jarak_tempuh), ".0f")
            self.jarak_tempuh_total = (
                self.jarak_tempuh_total + self.jarak_tempuh_total_lima
            )
            # self.jarak_tempuh_total = self.jarak_tempuh_total + jarak_tempuh

            self.total_odo = format(float(self.jarak_tempuh_total), ".3f")
            # self.root.ids.odometer.text = format(float(self.total_odo), ".3f")

            data_odo["total_km"] = self.total_odo
            self.update_database("odometer", data_odo)
            data_odo = self.read_database("odometer")
            odo = data_odo["total_km"]

            currentChannel = self.root.ids.channels.current
            if currentChannel == "mainChannel":
                self.root.ids.odometer_onMain.text = format(float(odo), ".3f")
            elif currentChannel == "mapChannel":
                self.root.ids.odometer_onMap.text = format(float(odo), ".3f")
            elif currentChannel == "aboutChannel":
                self.root.ids.odometer_onAbout.text = format(float(odo), ".3f")

    # percobaan dengan mendeteksi state dimana delta kecepatan sekarang dan kecepatan sebelumnya sangat besar
    #             delta_speed = float(self.kecepatan) - self.kecepatan_sebelum

    #             try:
    #                 if len(str(datadb)) != 0 and float(self.kecepatan) > 10.0 and delta_speed < 20:
    #                     file = "database/odometer.json"
    #                     with open(file, 'w') as file_object:
    #                         json.dump(odometer, file_object, indent=4)
    #                 # print(data_json)
    #             # else:
    #             #     print("Time out! Exit.\n")
    #             #     pass

    def modePressed(self):
        vehicleStatus = self.read_database("vehicle_info")
        mode_onMain = self.root.ids.mode_onMain
        if mode_onMain.text == "ECO":
            vehicleStatus["mode"] = "n"
            mode_onMain.text = "NORMAL"
        elif mode_onMain.text == "NORMAL":
            vehicleStatus["mode"] = "s"
            mode_onMain.text = "SPORT"
        else:
            vehicleStatus["mode"] = "e"
            mode_onMain.text = "ECO"
        self.update_database("vehicle_info", vehicleStatus)

    def turn_signal(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        vehicleStatus = self.read_database("vehicle_info")
        vehicleMode = vehicleStatus["mode"]
        isTurnLeft = vehicleStatus["turn_signal"][0]
        isTurnRight = vehicleStatus["turn_signal"][1]

        currentChannel = self.root.ids.channels.current

        if vehicleMode == "e":

            if currentChannel == "mainChannel":
                mode_onMain = self.root.ids.mode_onMain
                mode_onMain.text = "ECO"
        elif vehicleMode == "n":

            if currentChannel == "mainChannel":
                mode_onMain = self.root.ids.mode_onMain
                mode_onMain.text = "NORMAL"
        elif vehicleMode == "s":

            if currentChannel == "mainChannel":
                mode_onMain = self.root.ids.mode_onMain
                mode_onMain.text = "SPORT"

        if isTurnLeft == True:
            self.root.ids.turn_left.text_color = self.off
            Clock.schedule_once(self.blink_signal, 0.5)
        elif isTurnRight == True:
            self.root.ids.turn_right.text_color = self.off
            Clock.schedule_once(self.blink_signal, 0.5)
        else:
            self.root.ids.turn_left.text_color = self.dark_blue
            self.root.ids.turn_right.text_color = self.dark_blue

    def blink_signal(self, *args):
        self.root.ids.turn_left.text_color = self.dark_blue
        self.root.ids.turn_right.text_color = self.dark_blue

    def update_status(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        # tambah detik = :%S
        # self.root.ids.SOC_value.text = "blok"
        self.root.ids.time_onMain.text = strftime("[b]%H:%M  |[/b]")
        self.root.ids.time_onAbout.text = strftime("[b]%H:%M  |[/b]")
        self.root.ids.time_onMap.text = strftime("%H:%M")

        if self.root.ids.power_switch.active == False:
            vehicleStatus = self.read_database("vehicle_info")
            vehicleStatus["power"] = "off"
            self.update_database("vehicle_info", vehicleStatus)
            os.system("killall python3")
            os.system("killall python")

        fd = open("database/connection.json")
        connectionFile = json.load(fd)
        wifiID = connectionFile["wifi"]["id"]
        password = connectionFile["wifi"]["pass"]
        restartConnect = connectionFile["restart"]
        # print (tujuan)

        if len(wifiID) == 0:
            pass
            # self.root.ids.bluetooth_status.text_color = 15/255,18/255,23/255,1
        else:
            if len(password) == 0:
                pass
            else:
                # code disini
                # self.root.ids.bluetooth_status.text_color = 255/255,255/255,255/255,1
                if self.val != wifiID:
                    try:
                        self.root.connect(wifiID, password)
                        self.val = wifiID
                        # test = sub.out
                    except:
                        print("gagal untuk menyambungkan")
                        pass
                elif restartConnect == True:
                    Clock.schedule_once(self.root.connect(wifiID, password), 1)

                else:
                    pass

        fe = open("database/estimation.json")
        estimationFile = json.load(fe)
        asalLat = estimationFile["address"]["origin"]["latitude"]
        asalLng = estimationFile["address"]["origin"]["longitude"]
        tujuanLat = estimationFile["address"]["destination"]["latitude"]
        tujuanLng = estimationFile["address"]["destination"]["longitude"]

        if len(tujuanLat) == 0:
            pass
        else:
            if self.tuj != tujuanLat:
                # try:
                # fungsi tujuan
                try:
                    self.root.ids.mapview.remove_widget(self.root.marker)
                except:
                    pass

                try:
                    self.root.estimasi(
                        asalLat, asalLng, tujuanLat, tujuanLng, self.SOC_value
                    )
                except Exception as e:
                    print("estimation error :", str(e))

                self.screen_tomap = True
                self.root.center_maps()
                self.tuj = tujuanLat
                print("selesai")
                # except Exception as e:
                #     print('function error :',str(e) )
            else:
                pass


class MyLayout(Screen):
    wall_path = "assets/grad-wf.png"

    def __init__(self, *args, **kwargs):
        super(MyLayout, self).__init__(*args, **kwargs)

        this_path = str(os.getcwd())
        path = this_path + "/.key/api-key.txt"
        API_file = open(path, "r")
        # print(API_file)
        self.API_key = API_file.read()
        API_file.close()

    def center_maps(self):
        # try:
        mapview = self.ids.mapview
        line = LineMapLayer(
            self.DestinationLat, self.DestinationLng, self.OriginLat, self.OriginLng
        )
        mapview.add_layer(line, mode="scatter")
        print(self.OriginLat)
        print(self.OriginLng)

        # except Exception as e:
        #     print("error load map:", str(e))

        # try:
        mapview.center_on(float(self.OriginLat), float(self.OriginLng))
        # marker1 = MapMarkerPopup(lat=lat, lon=lng)

        # except Exception as e:
        #     print("error center map:", str(e))

        try:
            self.marker_origin = MapMarker(
                lat=self.OriginLat, lon=self.OriginLng, source="assets/marker-3-24.png"
            )
            self.marker_destination = MapMarker(
                lat=self.DestinationLat,
                lon=self.DestinationLng,
                source="assets/marker-red.png",
            )
            mapview.add_widget(self.marker_origin)
            mapview.add_widget(self.marker_destination)
            Clock.schedule_once(self.zoom_maps, 15)
            # mapview.add_marker(lat=lat, lon=lng)
        except Exception as e:
            print("error marker map:", str(e))

    def zoom_maps(self, *args):
        mapview = self.ids.mapview
        mapview.zoom = 14

    def move_speed(self):
        self.ids.channels.switch_to(self.ids.mainMenu)

    # def move_graph(self):
    #     self.ids.channels.switch_to(self.ids.test3, direction='left')

    def connect(self, name, password):
        try:
            self.commandl = "nmcli dev wifi connect " + name + " password " + password
            # print ("success connection : ",sub.out)
            # print (self.command1)
            scan = os.popen("nmcli device wifi list --rescan yes").read()
            isConnect = os.popen(self.commandl).read()
            # isConnect = True
        except:
            isConnect = ""

        if isConnect != "":
            self.popup = MDDialogDef(
                title="terhubung dengan internet \n wifi id : " + name,
                radius=[7, 7, 7, 7],
                md_bg_color=(25 / 255, 135 / 255, 84 / 255, 1),
                size_hint=(None, None),
                size=(400, 400),
            )
            self.root.ids.wifi_status.icon = "wifi-on"
            # self.root.ids.wifi_status.text_color = Dashboard.dark_blue
            self.root.ids.wifi_status.text_color = Dashboard.off_white
            self.popup.open()
        else:
            self.popup = MDDialogDef(
                title="tidak dapat terhubung dengan internet",
                text="kirim wifi id dan password kembali",
                radius=[7, 7, 7, 7],
                md_bg_color=(244 / 255, 67 / 255, 54 / 255, 1),
                size_hint=(None, None),
                size=(400, 400),
            )
            self.popup.open()
        # self.sub(self.commandl)

    # function to display avavilabe Wifi networks
    # def displayAvailableNetworks(self):
    #     self.commandl = "nmcli dev wifi"
    #     self.sub(self.commandl)

    # def sub(self,command):
    #     self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #     (out, err) = self.proc.communicate()
    #     print ("program output : ", out)
    #     print ("error : ",err)

    def move_s_mini1(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini1)

    def move_s_mini2(self):
        self.ids.screendget_mini.switch_to(self.ids.s_mini2)

    def estimasi(self, originLat, originLng, destinationLat, destinationLng, SOC_value):
        # gmaps = googlemaps.Client(key=API_key)

        scaler = joblib.load("estimation/std_rev1.bin")
        model = joblib.load("estimation/estimasi_rev1.pkl")

        self.DestinationLat = destinationLat
        self.DestinationLng = destinationLng
        self.OriginLat = originLat
        self.OriginLng = originLng
        body = {
            "locations": [
                [self.OriginLng, self.OriginLat],
                [self.DestinationLng, self.DestinationLat],
            ],
            "metrics": ["distance", "duration"],
            "units": "km",
        }
        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": self.API_key,
            "Content-Type": "application/json; charset=utf-8",
        }
        post_matrix = requests.post(
            "https://api.openrouteservice.org/v2/matrix/driving-car",
            json=body,
            headers=headers,
        )

        try:
            data_matrix = json.loads(post_matrix.text)
            duration = data_matrix["durations"][0][1]
            TrueDistance = data_matrix["distances"][0][1]
            TrueDistance = format(float(TrueDistance), ".3f")
            self.ids.DistanceEst.text = str(TrueDistance) + " km"
            duration_minute = float(duration) / 60
            duration_minute = format(float(duration_minute), ".2f")
            self.ids.TimeEst.text = str(duration_minute) + " menit"
        except Exception as e:
            print("INVALID REQUEST DISTANCE :", str(e))

        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        }
        get_geocode_origin = requests.get(
            "https://api.openrouteservice.org/geocode/reverse?api_key="
            + self.API_key
            + "&point.lon="
            + str(self.OriginLng)
            + "&point.lat="
            + str(self.OriginLat)
            + "&size=2",
            headers=headers,
        )
        get_geocode_destination = requests.get(
            "https://api.openrouteservice.org/geocode/reverse?api_key="
            + self.API_key
            + "&point.lon="
            + str(self.DestinationLng)
            + "&point.lat="
            + str(self.DestinationLat)
            + "&size=2",
            headers=headers,
        )

        # try:
        geocode_origin = json.loads(get_geocode_origin.text)
        geocode_destination = json.loads(get_geocode_destination.text)

        place_name_origin = geocode_origin["features"][0]["properties"]["label"]
        place_name_origin = place_name_origin.split(",")
        place_name_origin = place_name_origin[0:2]
        place_name_origin = ",".join(place_name_origin)

        place_name_destination = geocode_destination["features"][0]["properties"][
            "label"
        ]
        place_name_destination = place_name_destination.split(",")
        place_name_destination = place_name_destination[0:2]
        place_name_destination = ",".join(place_name_destination)

        self.ids.lokasi_label.text = "ASAL        :  %s\nTUJUAN   :  %s" % (
            place_name_origin,
            place_name_destination,
        )
        # print(call.status_code, call.reason)
        print(place_name_destination)
        # except Exception as e:
        #     print('INVALID REQUEST DISTANCE :',str(e) )

        # try:
        SOC_value = self.ids.SOC_circular.current_percent
        print("SOC : ", SOC_value)
        SOC = SOC_value
        # SOC = SOC_value.replace("%","")
        print(float(SOC))
        dm = open("database/speedmode.json")
        data_speedmode = json.load(dm)
        eco = data_speedmode["mode"]["eco"]
        normal = data_speedmode["mode"]["normal"]
        sport = data_speedmode["mode"]["sport"]
        speedmode = [eco, normal, sport]
        # except Exception as e:
        #     print('INVALID STORING DATA :',str(e) )

        try:
            length = TrueDistance
            for x in speedmode:
                coba = [[float(SOC), float(x), float(length)]]
                data = scaler.transform(coba)
                test = model.predict(data)
                print("estimasi pemakaian energi : ", float(x), float(test))
                if float(SOC) - (3 / 100) * 5 <= float(test):
                    if x == eco:
                        estimasi_eco = "TIDAK CUKUP"
                        self.ids.eco_recomm.color = 223 / 255, 91 / 255, 97 / 255, 1
                    elif x == normal:
                        estimasi_normal = "TIDAK CUKUP"
                        self.ids.normal_recomm.color = 223 / 255, 91 / 255, 97 / 255, 1
                    elif x == sport:
                        estimasi_sport = "TIDAK CUKUP"
                        self.ids.sport_recomm.color = 223 / 255, 91 / 255, 97 / 255, 1

                elif float(SOC) - (3 / 100) * 5 > float(test):
                    if x == eco:
                        estimasi_eco = "CUKUP"
                        self.ids.eco_recomm.color = 120 / 255, 184 / 255, 146 / 255, 1
                    elif x == normal:
                        estimasi_normal = "CUKUP"
                        self.ids.normal_recomm.color = (
                            120 / 255,
                            184 / 255,
                            146 / 255,
                            1,
                        )
                    elif x == sport:
                        estimasi_sport = "CUKUP"
                        self.ids.sport_recomm.color = 120 / 255, 184 / 255, 146 / 255, 1

            # satu rekomendasi
            self.ids.eco_recomm.text = str(estimasi_eco)
            self.ids.normal_recomm.text = str(estimasi_normal)
            self.ids.sport_recomm.text = str(estimasi_sport)
            self.popup = MDDialogMap(
                title="Estimasi telah dilakukan",
                text="ECO : "
                + estimasi_eco
                + "\nNORMAL :"
                + estimasi_normal
                + "\nSPORT :"
                + estimasi_sport,
                radius=[7, 7, 7, 7],
                md_bg_color=(25 / 255, 135 / 255, 84 / 255, 1),
                size_hint=(None, None),
                size=(400, 200),
            )
            self.popup.open()
        except Exception as e:
            print("estimation error ni :", str(e))
            self.popup = MDDialogMap(
                title="Estimasi gagal",
                text="pastikan kendaraan terkoneksi dengan internet",
                radius=[7, 7, 7, 7],
                md_bg_color=(244 / 255, 67 / 255, 54 / 255, 1),
                size_hint=(None, None),
                size=(400, 200),
            )
            self.popup.open()

        # tiga rekomendasi
        # self.ids.recommendation.text = "ECO          :  %s\n\nNORMAL  :  %s\n\nSPORT     :  %s" %(estimasi_eco, estimasi_normal, estimasi_sport)


class MDDialogDef(MDDialog):
    def __init__(self, **kwargs):
        super(MDDialog, self).__init__(**kwargs)
        # call dismiss_popup in 5 seconds
        Clock.schedule_once(self.dismiss_popup, 5)

    def dismiss_popup(self, *args):
        self.dismiss()


class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    duration = 3
    font_size = NumericProperty("18sp")
    radius = [10, 10, 10, 10]

    # def __init__(self, **kwargs):
    #     super(Snackbar, self).__init__(**kwargs)
    #     # call dismiss_popup in 5 seconds
    #     Clock.schedule_once(self.dismiss_popup, 5)

    # def dismiss_popup(self, *args):
    #     self.dismiss()


class MDDialogMap(MDDialog):
    def __init__(self, **kwargs):
        super(MDDialog, self).__init__(**kwargs)
        # call dismiss_popup in 15 seconds
        Clock.schedule_once(self.dismiss_popup, 15)

    def dismiss_popup(self, *args):
        self.dismiss()


class LineMapLayer(MapLayer):
    def __init__(self, lat, lng, OriginLat, OriginLng, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)

        this_path = str(os.getcwd())
        path = this_path + "/.key/api-key.txt"
        API_file = open(path, "r")
        print(API_file)
        self.API_key_map = API_file.read()
        API_file.close()
        # self.zoom = 16

        url = (
            "https://api.openrouteservice.org/v2/directions/driving-car?&api_key="
            + self.API_key_map
        )

        # testing Dummies
        # -7.289612, 112.796190

        start = "&start=" + str(OriginLng) + "," + str(OriginLat)
        end = "&end=" + str(lng) + "," + str(lat)

        final = url + start + end
        payload = {}
        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        }

        response = requests.request("GET", final, headers=headers, data=payload)
        hasil = json.loads(response.text)
        polyCoordinates = hasil["features"][0]["geometry"]["coordinates"]

        self._coordinates = [[polyCoordinates[0][1], polyCoordinates[0][0]]]
        for i in range(1, len(polyCoordinates)):
            # self.points =polyCoordinates[i-1], polyCoordinates[i]
            self.points = (polyCoordinates[i][1], polyCoordinates[i][0])
            self._coordinates.append(self.points)
        self._line_points = None
        self._line_points_offset = (0, 0)
        self.zoom = 8

        # geo_dover   = [51.126251, 1.327067]
        # geo_calais  = [50.959086, 1.827652]

        # # NOTE: Points must be valid as they're no longer clamped
        # self.coordinates = [geo_dover, geo_calais]
        # for i in range(25000-2):
        #     self.coordinates.append(self.gen_point())

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates
        self.invalidate_line_points()
        self.clear_and_redraw()

    @property
    def line_points(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points

    @property
    def line_points_offset(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset

    @property
    def line_points_offset(self):
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset

    def calc_line_points(self):
        # Offset all points by the coordinates of the first point, to keep coordinates closer to zero.
        # (and therefore avoid some float precision issues when drawing lines)
        self._line_points_offset = (
            self.get_x(self.coordinates[0][1]),
            self.get_y(self.coordinates[0][0]),
        )
        # Since lat is not a linear transform we must compute manually
        self._line_points = [
            (
                self.get_x(lon) - self._line_points_offset[0],
                self.get_y(lat) - self._line_points_offset[1],
            )
            for lat, lon in self.coordinates
        ]

    def invalidate_line_points(self):
        self._line_points = None
        self._line_points_offset = (0, 0)

    def get_x(self, lon):
        """Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) * self.ms / 360.0

    def get_y(self, lat):
        """Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        """
        lat = radians(clamp(-lat, MIN_LATITUDE, MAX_LATITUDE))
        return ((1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi)) * self.ms / 2.0

    def reposition(self):
        mapview = self.parent

        # Must redraw when the zoom changes
        # as the scatter transform resets for the new tiles
        if self.zoom != mapview.zoom:
            map_source = mapview.map_source
            self.ms = pow(2.0, mapview.zoom) * map_source.dp_tile_size
            self.invalidate_line_points()
            self.clear_and_redraw()

    def clear_and_redraw(self, *args):
        with self.canvas:
            # Clear old line
            self.canvas.clear()

        # FIXME: Why is 0.05 a good value here? Why does 0 leave us with weird offsets?
        Clock.schedule_once(self._draw_line, 0.05)

    def _draw_line(self, *args):
        mapview = self.parent
        self.zoom = 12
        self.zoom = mapview.zoom

        # When zooming we must undo the current scatter transform
        # or the animation distorts it
        scatter = mapview._scatter
        sx, sy, ss = scatter.x, scatter.y, scatter.scale
        vx, vy, vs = mapview.viewport_pos[0], mapview.viewport_pos[1], mapview.scale

        # Account for map source tile size and mapview zoom

        #: Since lat is not a linear transform we must compute manually
        line_points = []
        for lat, lon in self.coordinates:
            line_points.extend((self.get_x(lon), self.get_y(lat)))
            # line_points.extend(mapview.get_window_xy_from(lat,lon,mapview.zoom))

        with self.canvas:
            # Clear old line
            self.canvas.clear()

            # Undo the scatter animation transform
            Translate(*mapview.pos)
            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            # Apply the get window xy from transforms
            Scale(vs, vs, 1)
            Translate(-vx, -vy)

            # Apply the what we can factor out of the mapsource long, lat to x, y conversion
            Translate(self.ms / 2, 0)

            # Translate by the offset of the line points (this keeps the points closer to the origin)
            Translate(*self.line_points_offset)

            # Draw new
            # Color(31/255,146/255,161/255,1 )
            # Line(points=self.line_points, width=6/2, joint="round")#4/ms)#6., joint="round",joint_precision=100)
            # Color(146/255,218/255,241/255,1)
            Color(63 / 255, 146 / 255, 172 / 255, 1)
            Line(
                points=self.line_points, width=4 / 2, joint="round", joint_precision=100
            )


class NoValueSpeedMeter(SpeedMeter):
    def value_str(self, n):
        return ""


_displayed = {
    0: "0",
    30: "\u03a0 / 6",
    60: "\u03a0/3",
    90: "\u03a0/2",
    120: "2\u03a0/3",
    150: "5\u03a0/6",
    180: "\u03a0",
    210: "7\u03a0/6",
    240: "4\u03a0/3",
}


def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop

    if not EventLoop.event_listeners:
        from kivy.cache import Cache

        window.Window = window.core_select_lib("window", window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


# MyLayout.estimasi.has_been_called = False
# lay = MyLayout()
reset()
Dashboard().run()
try:
    os.system("killall python3")
except:
    os.system("killall python")
