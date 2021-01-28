from PIL import Image
import numpy as np

def make(mode, width, height, ls):
    _tmp=[]
    
    for i in ls:
        _tmp.append(tuple(int(x*255) for x in i))
    
    img = Image.new(mode, (width, height))
    img.putdata(_tmp)
    img.save('output_img.bmp')
