from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.relativelayout import RelativeLayout
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
    percent = NumericProperty(1)

    def __init__(self, constellation, **kwargs):
        super(Connection, self).__init__(**kwargs)
        self.constellation = constellation
        Window.on_resize = self.update_points
        self.update_points()

    def update_points(self, width=None, height=None):
        x0 = self.from_star.offset_x * self.constellation.width
        y0 = self.from_star.offset_y * self.constellation.height
        x1 = self.to_star.offset_x * self.constellation.width
        y1 = self.to_star.offset_y * self.constellation.height
        angle = math.atan2(y1-y0, x1-x0)
        length = math.sqrt((x1-x0)**2 + (y1-y0)**2) * self.percent
        p = [x0, y0, x0+math.cos(angle)*length, y0+math.sin(angle)*length]
        self.points = p


class Constellation(RelativeLayout):
    def __init__(self, **kwargs):
        super(Constellation, self).__init__(**kwargs)
        
        Window.on_resize = self.resize_constellation
        self.resize_constellation(Window.width, Window.height)

        stars = [Star(num=1, offset_x=.1, offset_y=.1, connects_to=[2]),
                 Star(num=2, offset_x=.2, offset_y=.3, connects_to=[3,6]),
                 Star(num=3, offset_x=.3, offset_y=.5, connects_to=[4,5]),
                 Star(num=4, offset_x=.6, offset_y=.6, connects_to=[]),
                 Star(num=5, offset_x=.4, offset_y=.4, connects_to=[3,6]),
                 Star(num=6, offset_x=.4, offset_y=.2, connects_to=[2,5])]

        self.loadConnections(stars)
        for star in stars:
            self.add_widget(star)

    def resize_constellation(self, width, height):
        length = min(width, height)
        self.size = [length, length]

    def loadConnections(self, stars):
        for from_star in stars:
            for connecting_num in from_star.connects_to:
                to_star = filter(lambda s: s.num == connecting_num, stars)[0]
                self.add_widget(Connection(self, from_star=from_star, to_star=to_star))


class ConstellationTracerApp(App):
    def build(self):
        constellation = Constellation()
        return constellation


if __name__ == '__main__':
    ConstellationTracerApp().run()
