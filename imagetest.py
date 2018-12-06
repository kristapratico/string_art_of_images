from PIL import Image
from PIL import ImageStat
from PIL import ImageColor
from PIL import ImageDraw
from bresenham import bresenham
import math
from math import pi
import numpy

def circle(radius):
    # init vars
    switch = 3 - (2 * radius)
    points = list()
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points.append((x,-y))
        # first quarter 2nd octant
        points.append((y,-x))
        # second quarter 3rd octant
        points.append((y,x))
        # second quarter 4.octant
        points.append((x,y))
        # third quarter 5.octant
        points.append((-x,y))
        # third quarter 6.octant
        points.append((-y,x))
        # fourth quarter 7.octant
        points.append((-y,-x))
        # fourth quarter 8.octant
        points.append((-x,-y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points

def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

# def fullprint(*args, **kwargs):
#     from pprint import pprint
#     import numpy
#     opt = numpy.get_printoptions()
#     numpy.set_printoptions(threshold='nan')
#     pprint(*args, **kwargs)
#     numpy.set_printoptions(**opt)


image = Image.open('cat.jpeg', 'r')
#width, height = image.size
#pixel_values = list(image.getdata())
pixel_values = get_image('cat.jpeg')
print len(pixel_values)


# im = Image.new('RGBA', (100, 100))
# im.getpixel((0, 0))
# for x in range(100):
#     for y in range(50):
#         im.putpixel((x, y), (210, 210, 210))

# for x in range(100):
#     for y in range(50, 100):
#        im.putpixel((x, y), ImageColor.getcolor('darkgray', 'RGBA'))

# im.getpixel((0, 0))

# im.getpixel((0, 50))
# im.save('putPixel.png')

# stat = ImageStat.Stat(image)
# mean = stat.mean
# print mean
# bre = list(bresenham(-238, 77, 2, 12))
# print bre
# for pix in bre:
#     print im.getpixel((pix))
#     im.putpixel(((pix)), ImageColor.getcolor('black', 'RGBA'))

# im.save('putPixel.png')

def points_on_circumference(center=(0, 0), r=150, n=700):
    return [
        (
            int(center[0] + (math.cos(2 * pi / n * x) * r)),  # x
            int(center[1] + (math.sin(2 * pi / n * x) * r))  # y

        ) for x in xrange(0, n + 1)]


coords = points_on_circumference(center=(145,150),r=130)
#print coords

# coords = circle(150)
# #points = numpy.array([[math.cos(numpy.pi*2*i/n), math.sin(numpy.pi*2*i/n)] for i in range(n)])


SQUARE_FIT_SIZE = 300.0
kitty = Image.open("cat.jpeg")
kittyWidth, kittyHeight = kitty.size


if kittyWidth > SQUARE_FIT_SIZE and kittyHeight > SQUARE_FIT_SIZE:
    # fix this 
    if kittyWidth > kittyHeight:
        kittyHeight = int((SQUARE_FIT_SIZE / kittyWidth) * kittyHeight)
        kittyWidth = SQUARE_FIT_SIZE
    else:           
        print kittyWidth, kittyHeight
        kittyWidth = (SQUARE_FIT_SIZE / kittyHeight) * kittyWidth
        kittyWidth = int(kittyWidth)
        kittyHeight = int(SQUARE_FIT_SIZE)
        print kittyWidth, kittyHeight


kitty = kitty.resize((kittyWidth, kittyHeight))


draw = ImageDraw.Draw(kitty)

for pix in coords:
    draw.point(((pix)), fill=(150))

# x=137
# y=150
# r=132
# draw.ellipse((x-r, y-r, x+r, y+r), outline=(150))

# draw.point((x-r, y-r, x+r, y+r), fill=(150))
# draw.point((85, 101), fill=(150))
# draw.point((270, 105), fill=(226))
draw.line([(274, 138), (40, 72)], fill=150)
bre = list(bresenham(int(274.4766582193811), int(138.3468898425535), int(40.51789151199743), int(72.64698450673521)))
for pix in bre:
    kitty.putpixel(((pix)), ImageColor.getcolor('black', 'RGBA'))
kitty.save("cat3.png")