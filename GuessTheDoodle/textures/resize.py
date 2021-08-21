import os
from os.path import isfile, join
import PIL
from PIL import Image

files = sorted([f for f in os.listdir("./doodles/") if isfile(join("./doodles/", f))])

for i,f in enumerate(files):
    im = Image.open("./doodles/"+f)
    print((int(im.size[0]/16),int(im.size[1]/16)))
    im = im.resize((int(im.size[0]/16),int(im.size[1]/16)), PIL.Image.ANTIALIAS)
    im.save('./doodles/'+str(i)+'.png')
