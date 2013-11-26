import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.graphics import Color, Ellipse
from kivy.vector import Vector
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
import math


class Star(Widget):
    offset_x = NumericProperty(0)
    offset_y = NumericProperty(0)
    num = NumericProperty(None)
    connects_to = ObjectProperty(None)
    connected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)
        self.bind(size=self.draw)
        self.bind(pos=self.draw)

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            sz = self.size[0]
            for r in range(sz, 8, -6):
                c = (sz-(r+2))/8.0
                Color(c*.2, c*.2, c)
                d = (sz-r)/2
                Ellipse(size=[r, r], pos=[self.pos[0]+d, self.pos[1]+d])

class Handle(Widget):
    connection = ObjectProperty(None)

    def __init__(self, connection, **kwargs):
        self.connection = connection
        super(Handle, self).__init__(**kwargs)


class Connection(Widget):
    from_star = ObjectProperty(None)
    to_star = ObjectProperty(None)
    points = ListProperty([0,0,0,0])
    percent = NumericProperty(0)
    end_pos = (0,0)
    constellation = None

    def __init__(self, constellation, **kwargs):
        super(Connection, self).__init__(**kwargs)
        self.constellation = constellation
        constellation.bind(size=self.update_points)
        self.bind(percent=self.percent_updated)

    def percent_updated(self, sender, percent):
        self.update_points(sender, self.constellation.size)
        if percent == 1:
            self.connect_star(self.to_star)

    def connect_star(self, star):
        star.connected = True
        # any connections to this star should be made from it instead
        for connection in self.constellation.connections:
            if connection.to_star is star and connection.percent == 0:
                connection.to_star = connection.from_star
                connection.from_star = star
                connection.percent = max(connection.percent, 0.2)

    def update_points(self, sender, size):
        width, height = size
        x0 = self.from_star.offset_x * width
        y0 = self.from_star.offset_y * height
        x1 = self.to_star.offset_x * width
        y1 = self.to_star.offset_y * height
        angle = math.atan2(y1-y0, x1-x0)
        length = math.sqrt((x1-x0)**2 + (y1-y0)**2) * self.percent
        self.end_pos = x0+math.cos(angle)*length, y0+math.sin(angle)*length
        self.points = [x0, y0, self.end_pos[0], self.end_pos[1]]

    def on_touch_down(self, touch):
        self.do_trace(touch)

    def on_touch_move(self, touch):
        self.do_trace(touch)

    def do_trace(self, touch):
        speed = .15
        max_dist = self.from_star.size[0] * 1.5
        dist = math.sqrt((touch.pos[0] - self.end_pos[0]) ** 2 + (touch.pos[1] - self.end_pos[1]) ** 2)
        if dist < max_dist and self.from_star.connected:
            self.percent = min(1, self.percent + speed)


class Constellation(RelativeLayout):
    connections = []

    def __init__(self, **kwargs):
        super(Constellation, self).__init__(**kwargs)

        self.stars = [
                        Star(num=1,  offset_x=0.20, offset_y=0.88, connects_to=[2]),
                        Star(num=2,  offset_x=0.14, offset_y=0.72, connects_to=[3]),
                        Star(num=3,  offset_x=0.22, offset_y=0.62, connects_to=[4,6]),
                        Star(num=4,  offset_x=0.19, offset_y=0.74, connects_to=[5]),
                        Star(num=5,  offset_x=0.30, offset_y=0.89, connects_to=[]),
                        Star(num=6,  offset_x=0.29, offset_y=0.54, connects_to=[7]),
                        Star(num=7,  offset_x=0.40, offset_y=0.28, connects_to=[8,18]),
                        Star(num=8,  offset_x=0.32, offset_y=0.06, connects_to=[9]),
                        Star(num=9,  offset_x=0.61, offset_y=0.11, connects_to=[10]),
                        Star(num=10, offset_x=0.52, offset_y=0.31, connects_to=[11]),
                        Star(num=11, offset_x=0.58, offset_y=0.53, connects_to=[12,13]),
                        Star(num=12, offset_x=0.47, offset_y=0.64, connects_to=[6]),
                        Star(num=13, offset_x=0.92, offset_y=0.54, connects_to=[14,16]),
                        Star(num=14, offset_x=0.87, offset_y=0.63, connects_to=[15]),
                        Star(num=15, offset_x=0.80, offset_y=0.71, connects_to=[]),
                        Star(num=16, offset_x=0.89, offset_y=0.44, connects_to=[17]),
                        Star(num=17, offset_x=0.84, offset_y=0.35, connects_to=[]),
                        Star(num=18, offset_x=0.46, offset_y=0.30, connects_to=[10]),
                    ]
        self.add_connections()
        self.add_stars()
        self.add_handles()
        self.start()

    def add_connections(self):
        for from_star in self.stars:
            for connecting_num in from_star.connects_to:
                to_star = filter(lambda s: s.num == connecting_num, self.stars)[0]
                connection = Connection(self, from_star=from_star, to_star=to_star)
                self.add_widget(connection)
                self.connections.append(connection)

    def add_stars(self):
        for star in self.stars:
            self.add_widget(star)

    def add_handles(self):
        for connection in self.connections:
            self.add_widget(Handle(connection))

    def start(self):
        self.connections[0].connect_star(self.connections[0].from_star)
        self.connections[0].percent = .2


class MainLayout(AnchorLayout):
    pass


class ConstellationTracerApp(App):
    def build(self):
        return MainLayout()
        

if __name__ == '__main__':
    ConstellationTracerApp().run()
