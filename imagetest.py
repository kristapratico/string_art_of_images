from PIL import Image
from PIL import ImageStat
from PIL import ImageColor
from PIL import ImageDraw
from bresenham import bresenham
import math
from math import pi
import random
import numpy




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

# image = Image.open('cat.jpeg', 'r')
#width, height = image.size
#pixel_values = list(image.getdata())
# pixel_values = get_image('cat.jpeg')
#print len(pixel_values)


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





# for pix in coords:
#     draw.point(tuple(pix), fill=(150))

# x=178
# y=158
# r=150
# draw.ellipse((x-r, y-r, x+r, y+r), outline=(150))

# draw.point((x-r, y-r, x+r, y+r), fill=(150))
# draw.point((85, 101), fill=(150))
# draw.point((270, 105), fill=(226))
#draw.line([(274, 138), (40, 72)], fill=150)


kitty = Image.open("kitty.PNG").convert('L')
draw = ImageDraw.Draw(kitty)
kitty.save("kitty1.png")


imgRadius = 500 


# if kittyWidth > SQUARE_FIT_SIZE and kittyHeight > SQUARE_FIT_SIZE:
#     # fix this 
#     if kittyWidth > kittyHeight:
#         kittyHeight = int((SQUARE_FIT_SIZE / kittyWidth) * kittyHeight)
#         kittyWidth = SQUARE_FIT_SIZE
#     else:           
#         #print kittyWidth, kittyHeight
#         kittyWidth = (SQUARE_FIT_SIZE / kittyHeight) * kittyWidth
#         kittyWidth = int(kittyWidth)
#         kittyHeight = int(SQUARE_FIT_SIZE)
#         #print kittyWidth, kittyHeight

height, width = kitty.size
minEdge= min(height, width)
topEdge = int((height - minEdge)/2)
leftEdge = int((width - minEdge)/2)
imgCropped = kitty.crop(())

imgCropped = kitty[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]
imgResized = imgCropped.resize((2*imgRadius + 1, 2*imgRadius + 1))
imgResized.save("kittycrop.png")
exit(1)

im = Image.new('RGB', (int(width), height), 'white')
catstr = ImageDraw.Draw(im)

kitty = cv2.resize(imgCropped, (2*imgRadius + 1, 2*imgRadius + 1)) 
cv2.imwrite('./resized.png', kitty)

height, width = kitty.shape[:2]
previousPins = []
imgResult = 255 * np.ones((height, width))
nLines = 900
nPins = 200
oldPin = 0
minLoop = 3
height, width = kitty.shape[0:2]
x = int(width/2)
y = int(height/2)

def make_circle(center=(0, 0), r=150, n=200):
    point = np.array([[int(center[0] + math.cos(np.pi*2*i/n) * r), int(center[1] + math.sin(np.pi*2*i/n) * r)] for i in range(n)])
    return point

def check_tooclose(coords, line, adj):
    if abs(line- adj) < 25:
        return True

coords = make_circle(center=(x,y),r=500)


line_list = []

for line in range(nLines):
    bestLine = 9999999999
    oldCoord = coords[oldPin]

    for index in range(1, nPins):
        pin = (oldPin + index) % nPins
        pixels = list()
        coord = coords[pin]
        if check_tooclose(coords, oldPin, pin):
            continue
        bre = list(bresenham(oldCoord[0], oldCoord[1], coord[0], coord[1]))
        for x in bre:
            y, z = x
            pixels.append(int(kitty[y, z]))
        lineSum = int(np.sum(pixels) / len(bre)) 
        if lineSum < bestLine:
            bestLine = lineSum
            bestPin = pin
            bestBre = bre
        # if (lineSum < bestLine) and not(pin in previousPins):
        #     bestLine = lineSum
        #     bestPin = pin
        #     bestBre = bre

    # Update previous pins
    # if len(previousPins) >= minLoop:
    #     previousPins.pop(0)
    # previousPins.append(bestPin)

    line_list.append((oldPin, bestPin))
    #cv2.line(kitty, tuple(oldCoord), tuple(coords[bestPin]), (255,255,255), 1)
    #cv2.line(imgResult, tuple(oldCoord), tuple(coords[bestPin]), (15,15,15),1)
    #pinn = coords[bestPin]
    #bre = list(bresenham(oldCoord[0], oldCoord[1], pinn[0], pinn[1]))
    for x in bestBre:
        y, z = x
        kitty[y, z] = 255
        imgResult[y, z] = 0
    # Save line to results
    # lines.append((oldPin, bestPin))

    # plot results
    # xLine, yLine = linePixels(coords[bestPin], coord)
    # imgResult[yLine, xLine] = 0

    # Break if no lines possible
    if bestPin == oldPin:
        break


    oldPin = bestPin

cv2.imwrite('lol5.png', kitty)
cv2.imwrite('threaded5.png', imgResult)



kitty.save("kit1.png")
im.save("kit2.png")