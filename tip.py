#!/usr/bin/python
# resize an image using the PIL image library
from PIL import Image
import sys

# Check argument length
if len(sys.argv) < 2:
    print("Please specify an image")
    exit()

# open image file
# (.bmp,.jpg,.png,.gif supported by PIL)
imageFile = sys.argv[1]
img = Image.open(imageFile)

# adjust width and height to your needs - 32 MAX
maxSize = 64
width = img.size[0]
height = img.size[1]

if width > height:
    ratio = int(width/maxSize)
else:
    ratio = int(height/maxSize)

width = int(width / ratio)
height =int(height / ratio)

img = img.resize((width, height), Image.ANTIALIAS)

pixels = img.load()
for y in range(0, img.size[1], 2):
    for x in range(img.size[0]):
        r, g, b = pixels[x, y]
        backgroundCode = (16 + (36 * int(r/51)) + (6 * int(g/51)) + int(b/51))

        r, g, b = pixels[x, y+1]
        forgroundCode = (16 + (36 * int(r/51)) + (6 * int(g/51)) + int(b/51))

        #sys.stdout.write("%3d;%3d;%3d %x\n" % (r, g, b, colorCode)) # DEBUG
        sys.stdout.write("\x1b[48;5;%d;38;5;%dm%s\x1b[0m" % (backgroundCode, forgroundCode, u"\u2584"))
    print("")

