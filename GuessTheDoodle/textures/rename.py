import os
from os.path import isfile, join
from PIL import Image, ImageDraw, ImageFont

files = sorted([f for f in os.listdir("./doodles/") if isfile(join("./doodles/", f))])

for i,f in enumerate(files):
    os.rename('./doodles/'+f, './doodles/'+String.format("%02d", i)+'.png')

W,H = 724,292
for i,f in enumerate(files):
    image = Image.new("RGB", (W,H), color='#f9efee')

    draw = ImageDraw.Draw(image)

    font1 = ImageFont.truetype('Roboto-Regular.ttf', size=H*3//20)
    font2 = ImageFont.truetype('Roboto-Bold.ttf', size=H//5)

    message = "THE ANSWER IS"
    w, _ = draw.textsize(message, font=font1)
    (x, y) = ((W-w)/2, H//4)
    color = '#f68aca'
    draw.text((x, y), message, fill=color, font=font1)

    name = f[:-4].upper()
    color = '#a5407c'
    w, _ = draw.textsize(name, font=font2)
    draw.text(((W-w)/2,H//2), name, fill=color, font=font2)

    image.save('./answers/'+String.format("%02d", i)+'.png', optimize=True, quality=20)
