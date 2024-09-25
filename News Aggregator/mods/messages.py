from math import sin, cos, pi

from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.button import MDFlatButton

from kivy.clock import Clock


########### LOADING SPINNER CLASS #############

class WaitingSpinner(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 100
        self.circle_count = 15
        self.small_circle_radius = 8
        self.animation_duration = 1
        self.angle_offset = 0

        self.circles = []
        self.create_circles()
        Clock.schedule_interval(self.update, 1 / 60)

    def create_circles(self):
        with self.canvas:
            for i in range(self.circle_count):
                angle = 2 * pi * i / self.circle_count
                x = self.center_x + self.radius * cos(angle) - self.small_circle_radius
                y = self.center_y + self.radius * sin(angle) - self.small_circle_radius

                Color(252/255, 226/255, 5/255)
                ellipse = Ellipse(pos=(x, y), size=(self.small_circle_radius * 2, self.small_circle_radius * 2))
                self.circles.append(ellipse)

    def update(self, dt):
        self.angle_offset += dt / self.animation_duration * 2 * pi

        for i, circle in enumerate(self.circles):
            angle = 2 * pi * i / self.circle_count + self.angle_offset
            x = self.center_x + self.radius * cos(angle) - self.small_circle_radius
            y = self.center_y + self.radius * sin(angle) - self.small_circle_radius
            circle.pos = (x, y)

    def on_size(self, *args):
        self.create_circles()
        

########### ERROR MESSAGES DIALOG #############


class ErrorDialog(MDDialog):
    pass
    

def show_error_message(text):
    dialog = ErrorDialog(
                title = f"[color=FFEB3B]News Aggregator[/color]", 
                text = f"[color=EEDC82]{text}[/color]",
                type = "custom",
                auto_dismiss = False,
                        
                buttons = [
                    MDFlatButton(
                        text = "OKAY",
                        theme_text_color = "Custom",
                        text_color = "FFA500",
                        pos_hint = {'center_x': .5, 'center_y': .5},
                        on_release = lambda _: dialog.dismiss(),
                        ),
                ],
            )
            
    dialog.open()
   
          