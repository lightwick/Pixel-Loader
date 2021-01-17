from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from random import random
from kivy.properties import StringProperty
from kivy.uix.button import Button
from imgLoad import Desktop_FileDialog, FileGroup

texture_width, texture_height = 0, 0

class box(Widget):
    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.pixel_size = 20
        self.x = 0
        self.y = 0
        self.w = self.h = self.pixel_size

        
        with self.canvas:
            Color(random(),random(),random())
            self.line = Line(rectangle=(self.x, self.y, self.w, self.h), width=2)

            
    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.canvas.remove(self.line)
        if keycode[1] == 'up':
            self.y+=10
        elif keycode[1] == 'down':
            self.y-=10
        elif keycode[1] == 'left':
            self.x-=10
        elif keycode[1] == 'right':
            self.x+=10
        with self.canvas:
            self.line = Line(rectangle=(self.x, self.y, self.w, self.h),width=2)

    def reposition(self):
        window_width, window_height = Window.size
        
        global texture_width, texture_height
        self.x = max(window_width/2-texture_width/2,0)
        self.y = min(window_height/2+texture_height/2-self.h, window_height-self.h)
        
        self.canvas.remove(self.line)
        with self.canvas:
            self.line = Line(rectangle=(self.x, self.y, self.w, self.h), width=2)
        
class img(Image):
    def __init__(self, **kwargs):
        super(img,self).__init__(**kwargs)
        self.source = "./starting_screen.png"
        
    def load(self, src):
        self.source = src
        self.reload()
        global texture_width, texture_height
        texture_width, texture_height = self.texture_size
        
class pixeller(App):
    def build(self):
        self.game = FloatLayout()
        
        self.image = img()
        self.box = box()
        #image.reload()
        self.game.add_widget(self.image)
        self.game.add_widget(self.box)
        img_btn = Button(text="Load IMG", size_hint = (.1,.1))      
        img_btn.bind(on_release = self.load_img)
        self.game.add_widget(img_btn)
        
        return self.game

    def load_img(self, obj):
        file_path = Desktop_FileDialog(
                title             = "Select File",
                initial_directory = "",
                file_groups = [
                    FileGroup(name="Image Files", extensions=["jpg", "jpeg", "png", "gif"]),
                    FileGroup.All_FileTypes,
                ],
            ).show()
        if file_path:
            self.image.load(file_path)
            self.box.reposition()
        
    def on_stop(self):
        Window.close()
        
if __name__ == "__main__":
    pixeller().run()
