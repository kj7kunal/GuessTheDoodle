from quickdraw import QuickDrawData
from PIL import Image, ImageDraw

CLASSES_PATH = "./classes.txt"
TOTALFRAMES = 30
BOXSIZE = 256
RETRIES_ALLOWED = 3
SAVE_PATH = "./generated/{}.png"


with open(CLASSES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

c = 0
retries = 0
while (c < len(classes)):
    # get random doodle of class
    print(f"Getting {c} doodle.")
    qd = QuickDrawData()
    doodle = qd.get_drawing(classes[c])

    # number of frames for doodle
    n = sum([len(s) for s in doodle.strokes]) - len(doodle.strokes)
    print(f"{n} frames in this doodle")

    # initialize empty PIL Images
    doodle_image = Image.new("L", ((TOTALFRAMES + 2) * BOXSIZE, BOXSIZE), color=255)
    part_image = Image.new("L", (BOXSIZE, BOXSIZE), color=255)
    doodle_drawing = ImageDraw.Draw(part_image)

    rem, pad = 0, 2
    if n > TOTALFRAMES:
        # Need to skip some frames to match TOTALFRAMES
        rem = n - TOTALFRAMES
        print(f"Removing {rem} frames")
    elif n < TOTALFRAMES:
        # Small drawing -> retry with another random doodle
        if retries < RETRIES_ALLOWED:
            retries += 1
            continue
        else:
            c += 1
            retries = 0
            continue
        # Need to duplicate some frames to match TOTALFRAMES
        # pad += TOTALFRAMES - n
        # print(f"Adding {pad} more frames")
    retries = 0

    i, xcoord = 0, 0
    for stroke in doodle.strokes:
        for coordinate in range(len(stroke) - 1):
            x1 = stroke[coordinate][0]
            y1 = stroke[coordinate][1]
            x2 = stroke[coordinate + 1][0]
            y2 = stroke[coordinate + 1][1]
            doodle_drawing.line((x1, y1, x2, y2), fill=0, width=4)

            if not(i%2 == 0 and rem > 0):
                doodle_image.paste(part_image.resize((BOXSIZE, BOXSIZE)).convert('L'), (xcoord, 0))
                xcoord += BOXSIZE
            else:
                rem -= 1
            i += 1

    # Add padding for extra timestamps in the end
    while(pad > 0):
        doodle_image.paste(part_image.resize((BOXSIZE, BOXSIZE)).convert('L'), (xcoord, 0))
        xcoord += BOXSIZE
        pad -= 1

    doodle_image.save(SAVE_PATH.format(str(classes[c])))
    print((xcoord//BOXSIZE), " = ", (TOTALFRAMES + 2))

    c += 1
