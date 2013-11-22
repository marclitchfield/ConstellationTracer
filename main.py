import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
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


class Connection(Widget):
    from_star = ObjectProperty(None)
    to_star = ObjectProperty(None)
    points = ListProperty(None)
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

    def on_touch_move(self, touch):
        error_distance = 10
        if abs(touch.pos[0] - self.end_pos[0]) < error_distance and abs(touch.pos[1] - self.end_pos[1]) < error_distance:
            self.percent = min(1, self.percent + .1)


class Constellation(RelativeLayout):

    def __init__(self, **kwargs):
        super(Constellation, self).__init__(**kwargs)

        stars = [Star(num=1, offset_x=.1, offset_y=.1, connects_to=[2]),
                 Star(num=2, offset_x=.2, offset_y=.3, connects_to=[3,6]),
                 Star(num=3, offset_x=.3, offset_y=.5, connects_to=[4,5]),
                 Star(num=4, offset_x=.6, offset_y=.6, connects_to=[]),
                 Star(num=5, offset_x=.4, offset_y=.4, connects_to=[3,6]),
                 Star(num=6, offset_x=.4, offset_y=.2, connects_to=[2,5])]

        connections = list(self.load(stars))
        connections[0].percent = 0.2

    def load(self, stars):
        for from_star in stars:
            for connecting_num in from_star.connects_to:
                to_star = filter(lambda s: s.num == connecting_num, stars)[0]
                connection = Connection(self, from_star=from_star, to_star=to_star)
                self.add_widget(connection)
                yield connection
        for star in stars:
            self.add_widget(star)


class MainLayout(AnchorLayout):
    pass


class ConstellationTracerApp(App):
    def build(self):
        return MainLayout()
        

if __name__ == '__main__':
    ConstellationTracerApp().run()
