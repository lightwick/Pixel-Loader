# Shorcomings:
# for now, it only works on images which the full textures fit within the window


from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'resizable', '0')
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.core.image import Image as CoreImage
from imgLoad import Desktop_FileDialog, FileGroup

from random import random

texture_width, texture_height = 0, 0
box_size_val = 20

box1_x, box1_y, box2_x, box2_y = 0, 0, 0, 0

# debug_x & debug_y relative coordinates of image
debug_x, debug_y = 0, 0
_color = 0,0,0,0

'''
class getPixel(Widget):
    def __init__(self, **kwargs):
        super(getPixel, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if box1_x
'''
class debug(Widget):
    def __init__(self, **kwargs):
        super(debug, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        global _color
        with self.canvas:
            self.rect = Rectangle(pos = (50,50), size=(100,100))
        '''
        with self.canvas:
            Color(0.25098039215686274, 0.0, 0.01568627450980392, 1.0)
            self.rect = Rectangle(pos = (50,50), size=(100,100))
        '''
    def _keyboard_closed(self):
        pass
        #self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        #self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        
        self.canvas.remove(self.rect)
        
        with self.canvas:
            Color(rgb=_color)
            self.rect = Rectangle(pos = (50,50), size=(100,100))

# the box's bottom left is it's x,y value
class box(Widget):
    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        global box_size_val
        self.x = 0
        self.y = 0
        self.box1_selected = False
        self.box2_selected = False
        self.box1 = Line()
        self.box2 = Line()
        with self.canvas:
            Color(random(),random(),random())
            self.line = Line(rectangle=(self.x, self.y, box_size_val, box_size_val), width=2)

            
    def _keyboard_closed(self):
        pass
        #self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        #self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # what this does:
        # 1. move the coordiantes of the box
        # 2. gets the coordinates of box1 & box2; stored in global variables box1_x, box1_x, box2_x, box2_y
        # 3. draws box1 & box2 when selected
        # 4. deletes box when 'esc' key is pressed
        
        # due to bug, widget pos moves with box
        global box1_x, box1_x, box2_x, box2_y

        global debug_x, debug_y

        self.canvas.remove(self.line)
        # needs configuratino with coordinates plus box_size_val
        if keycode[1] == 'up':
            if debug_y+box_size_val/2+5<texture_height:
                self.y+=5
                debug_y+=5
        elif keycode[1] == 'down':
            if debug_y+box_size_val/2-5>=0:
                self.y-=5
                debug_y-=5
        elif keycode[1] == 'left':
            if debug_x+box_size_val/2-5>=0:
                self.x-=5
                debug_x-=5
        elif keycode[1] == 'right':
            if debug_x+box_size_val/2+5<texture_width:
                self.x+=5
                debug_x+=5
                    
        with self.canvas:
            self.line = Line(rectangle=(self.x, self.y, box_size_val, box_size_val),width=2)


        if keycode[1] == 'enter':
            if self.box1_selected:
                box2_x, box2_y = self.pos
                self.box2_selected = True
                with self.canvas:
                    Color(random(),random(),random())
                    self.box2 = Line(rectangle=(self.x, self.y, box_size_val, box_size_val), width=2)
            else:
                box1_x, box1_y = self.pos
                self.box1_selected = True
                with self.canvas:
                    Color(random(),random(),random())
                    self.box1 = Line(rectangle=(self.x, self.y, box_size_val, box_size_val), width=2)
        elif keycode[1] == 'escape':
            if self.box1_selected:
                if self.box2_selected:
                    self.box2_selected = False
                    self.canvas.remove(self.box2)
                else:
                    self.box1_selected = False
                    self.canvas.remove(self.box1)

    def reposition(self):
        window_width, window_height = Window.size
        global texture_width, texture_height, box_size_val

        global debug_y
        # wanted to set upper left as (0,0), but when the box is redrawn with a different size, the bottom left becomes the datum point, so it's really hard to get by
        debug_y = texture_height-1-box_size_val
        self.x = max(window_width/2-texture_width/2,0)
        self.y = min(window_height/2+texture_height/2-box_size_val, window_height-box_size_val)

        self.canvas.remove(self.line)
        with self.canvas:
            self.line = Line(rectangle=(self.x, self.y, box_size_val, box_size_val), width=2)
            
class img(Image):
    def __init__(self, **kwargs):
        super(img,self).__init__(**kwargs)
        self.keep_data = True
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.source = "./starting_screen.png"
        
    def load(self, src):
        self.source = src
        self.keep_data=True
        self._coreimage.load(src, keep_data=True)
        self.reload()
        global texture_width, texture_height
        global box1_x, box1_y
        texture_width, texture_height = self.texture_size

    def _keyboard_closed(self):
        pass
        #self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        #self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers): # get the color of the changed
        global box_size_val, _color
        
        global texture_height
        # Holy shit it works!!!!
        # The problem was, the bottom left start as (0,0) where I thought the upper left was (0,0)
        # well shit, in the image the upper left is (0,0) and kivy objects, bottom left is (0,0) wtf
        _color = self._coreimage.read_pixel(debug_x+box_size_val/2, texture_height-(debug_y+box_size_val/2)-1)
        
        
class box_size(Slider):
    def __init__(self, **kwargs):
        super(box_size, self).__init__(**kwargs)
        self.bind(value = self.on_value)
        self.range = (10,50)
        self.value = 20
        self.value_track = True
        self.value_track_color=[random(), random(), random(), 1]
        self.step = 2
        # I don't know why top 0.65 would get it mostly in the bottom
        self.pos_hint={'top': .65}
        
        
    def on_value(self, obj, value):
        global box_size_val
        box_size_val = value
        
class pixeller(App):
        
    def build(self):
        self.game = FloatLayout()

        _debug = debug()
        self.image = img()
        self.box = box()
        #image.reload()
        self.game.add_widget(_debug)
        self.game.add_widget(self.image)
        self.game.add_widget(self.box)
        # while index isn't specified, widgets added last fires first

        s = box_size()
        self.game.add_widget(s)

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
