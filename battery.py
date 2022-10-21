from kivy.graphics import Color, Line, SmoothLine, RoundedRectangle


class batteryWidget(object):
    red = 223 / 255, 91 / 255, 97 / 255, 1
    green = 118 / 255, 209 / 255, 155 / 255, 1
    cyan = 126 / 255, 212 / 255, 240 / 255, 1
    dark_blue = 12 / 255, 49 / 255, 62 / 255, 1
    off = 180 / 255, 180 / 255, 180 / 255, 1
    off_white = 217 / 255, 217 / 255, 217 / 255, 1

    def __init__(
        self,
        status,
        batt_0,
        batt_1,
        batt_2,
        batt_3,
        batt_4,
    ):
        self.batt_0 = batt_0
        self.batt_1 = batt_1
        self.batt_2 = batt_2
        self.batt_3 = batt_3
        self.batt_4 = batt_4
        # self.batt_case = batt_case
        # self.batt_head = batt_head
        if status == 0:
            self.batt_low()
        elif status == 1:
            self.batt_below_average()
        elif status == 2:
            self.batt_average()
        elif status == 3:
            self.batt_above_average()
        elif status == 4:
            self.batt_full()

    def batt_low(self):
        # self.batts_case("low")
        # self.batts_head("low")
        self.batts_0("low")
        self.batts_1("off")
        self.batts_2("off")
        self.batts_3("off")
        self.batts_4("off")

    def batt_below_average(self):
        # self.batts_case("low")
        # self.batts_head("low")
        self.batts_0("low")
        self.batts_1("low")
        self.batts_2("off")
        self.batts_3("off")
        self.batts_4("off")

    def batt_average(self):
        # self.batts_case("on")
        # self.batts_head("on")
        self.batts_0("on")
        self.batts_1("on")
        self.batts_2("on")
        self.batts_3("off")
        self.batts_4("off")

    def batt_above_average(self):
        # self.batts_case("on")
        # self.batts_head("on")
        self.batts_0("on")
        self.batts_1("on")
        self.batts_2("on")
        self.batts_3("on")
        self.batts_4("off")

    def batt_full(self):
        # self.batts_case("on")
        # self.batts_head("on")
        self.batts_0("on")
        self.batts_1("on")
        self.batts_2("on")
        self.batts_3("on")
        self.batts_4("on")

    def batts_0(self, status):
        if status == "low":
            with self.batt_0.canvas:
                self.batt_0.canvas.clear()
                self.batt_0.canvas.add(Color(rgba=self.red))
                self.batt_0.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_0.pos,
                        size=self.batt_0.size,
                        radius=[(0, 0), (0, 0), (5, 5), (5, 5)],
                    )
                )
        elif status == "off":
            with self.batt_0.canvas:
                self.batt_0.canvas.clear()
        else:
            with self.batt_0.canvas:
                self.batt_0.canvas.clear()
                self.batt_0.canvas.add(Color(rgba=self.green))
                self.batt_0.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_0.pos,
                        size=self.batt_0.size,
                        radius=[(0, 0), (0, 0), (5, 5), (5, 5)],
                    )
                )

    def batts_1(self, status):
        if status == "low":
            with self.batt_1.canvas:
                self.batt_1.canvas.clear()
                self.batt_1.canvas.add(Color(rgba=self.red))
                self.batt_1.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_1.pos,
                        size=self.batt_1.size,
                        radius=[(0, 0), (0, 0), (0, 0), (0, 0)],
                    )
                )
        elif status == "off":
            with self.batt_1.canvas:
                self.batt_1.canvas.clear()
        else:
            with self.batt_1.canvas:
                self.batt_1.canvas.clear()
                self.batt_1.canvas.add(Color(rgba=self.green))
                self.batt_1.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_1.pos,
                        size=self.batt_1.size,
                        radius=[(0, 0), (0, 0), (0, 0), (0, 0)],
                    )
                )

    def batts_2(self, status):
        if status == "off":
            with self.batt_2.canvas:
                self.batt_2.canvas.clear()
        else:
            with self.batt_2.canvas:
                self.batt_2.canvas.clear()
                self.batt_2.canvas.add(Color(rgba=self.green))
                self.batt_2.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_2.pos,
                        size=self.batt_2.size,
                        radius=[(0, 0), (0, 0), (0, 0), (0, 0)],
                    )
                )

    def batts_3(self, status):
        if status == "off":
            with self.batt_3.canvas:
                self.batt_3.canvas.clear()
        else:
            with self.batt_3.canvas:
                self.batt_3.canvas.clear()
                self.batt_3.canvas.add(Color(rgba=self.green))
                self.batt_3.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_3.pos,
                        size=self.batt_3.size,
                        radius=[(0, 0), (0, 0), (0, 0), (0, 0)],
                    )
                )

    def batts_4(self, status):
        if status == "low":
            with self.batt_4.canvas:
                self.batt_4.canvas.clear()
                self.batt_4.canvas.add(Color(rgba=self.red))
                self.batt_4.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_4.pos,
                        size=self.batt_4.size,
                        radius=[(5, 5), (5, 5), (0, 0), (0, 0)],
                    )
                )
        elif status == "off":
            with self.batt_4.canvas:
                self.batt_4.canvas.clear()
        else:
            with self.batt_4.canvas:
                self.batt_4.canvas.clear()
                self.batt_4.canvas.add(Color(rgba=self.green))
                self.batt_4.canvas.add(
                    RoundedRectangle(
                        pos=self.batt_4.pos,
                        size=self.batt_4.size,
                        radius=[(5, 5), (5, 5), (0, 0), (0, 0)],
                    )
                )
