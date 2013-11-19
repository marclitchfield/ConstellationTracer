from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget

class Star(Widget):
    altitude = NumericProperty(0)
    azimuth = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Star, self).__init__(**kwargs)

class Constellation(RelativeLayout):
    def __init__(self, **kwargs):
        super(Constellation, self).__init__(**kwargs)
        
        Window.on_resize = self.resize_constellation
        self.resize_constellation(Window.width, Window.height)

        self.add_widget(Star(altitude=.1, azimuth=.1))
        self.add_widget(Star(altitude=.2, azimuth=.2))
        self.add_widget(Star(altitude=.3, azimuth=.5))

    def resize_constellation(self, width, height):
        length = min(width, height)
        self.size = [length, length]

    def update(self, dt):
        pass

class ConstellationTracerApp(App):
    def build(self):
        constellation = Constellation()
        Clock.schedule_interval(constellation.update, 1.0/60.0)
        return constellation

if __name__ == '__main__':
    ConstellationTracerApp().run()
