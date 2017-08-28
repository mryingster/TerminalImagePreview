#!/usr/bin/env python
import sys, os

def error(message):
    print("ERROR: "+message)
    quit(1)

def warning(message):
    print("WARNING: "+message)

try:
    from PIL import Image
except:
    error("Unable to load 'pil', or 'pillow'. Try 'sudo pip install pillow'.")

def getFileExtension(fileName):
    import re
    return re.compile('.*\.([^\.]*)').sub(r'\1', os.path.basename(fileName))

def help():
    #     0        10        20        30        40        50        60        70        80
    #     |---------|---------|---------|---------|---------|---------|---------|---------|
    print("Terminal Image Preview (tip.py)")
    print("")
    print("DESCRIPTION")
    print("    This tool will display an image to the screen using ANSI colors.")
    print("")
    print("SYNTAX")
    print("    tip.py <filename> <options>")
    print("")
    print("OPTIONS")
    print("    -h, --help    Show help screen")
    print("    -m  <integer> Specify MAX image size")
    print("")
    quit()

def to216color(r, g, b):
    return (16 + (36 * int(r/51)) + (6 * int(g/51)) + int(b/51))

def main(*inputArgs):
    # Can't pop tuple, so args convert to list
    arguments = list(inputArgs)
    supportedExtenions = ["jpg", "jpeg", "png", "gif", "tiff", "tif"]
    inputFiles = []
    maxSize = 64

    # Process arguments
    while len(arguments) > 0:
        argument = arguments[0]
        if argument == "-h" or argument == "--help":
            help()
        if os.path.exists(argument):
            if getFileExtension(argument).lower() in supportedExtenions:
                inputFiles.append(argument)
            else:
                warning("Invalid file type or argument, %s." % argument)
            arguments.pop(0)
        if argument == "-m":
            maxSize = int(arguments[1])
            if maxSize < 1:
                error("Please specify positive integer for maximum size.")
            arguments.pop(0)
            arguments.pop(0)

    # Make sure we have a file to process
    if len(inputFiles) < 1:
        error("Please specify an image")

    # Process each input image
    for path in inputFiles:
        # open image file
        try:
            img = Image.open(path)
        except:
            warning("Unable to open image, %s." % path)
            continue

        # adjust image width and height
        width = img.size[0]
        height = img.size[1]

        if width > height:
            ratio = int(width/maxSize)
        else:
            ratio = int(height/maxSize)

        width = int(width / ratio)
        height = int(height / ratio)

        # Make sure height is even number!
        if height % 2 != 0: height += 1

        # Resize
        img = img.resize((width, height), Image.ANTIALIAS)

        # Print image to screen using ANSI colors (216 colors)
        print(path)
        pixels = img.load()
        for y in range(0, img.size[1], 2):
            for x in range(img.size[0]):
                backgroundCode = to216color(*pixels[x, y][0:3])
                forgroundCode = to216color(*pixels[x, y+1][0:3])
                #sys.stdout.write("%3d;%3d;%3d %x\n" % (r, g, b, colorCode)) # DEBUG
                sys.stdout.write("\x1b[48;5;%d;38;5;%dm%s\x1b[0m" % (backgroundCode, forgroundCode, u"\u2584"))
            print("")
        print("")

if __name__ == "__main__":
    sys.argv.pop(0)
    main(*sys.argv)
