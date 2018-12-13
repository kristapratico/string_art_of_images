import math
import numpy as np
import cv2
import time


def bresenham(x0, y0, x1, y1):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    https://pypi.org/project/bresenham/
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy


def make_circle(center=(0, 0), r=150, n=200):
    point = np.array([[int(center[0] + math.cos(np.pi*2*i/n) * r), int(center[1] + math.sin(np.pi*2*i/n) * r)] for i in range(n)])
    return point

def check_tooclose(coords, line, adj):
    if abs(line- adj) < 25:
        return True

def update_image(breList, kitty, imgResult):
    for x in breList:
        y, z = x
        kitty[y, z] = 255
        imgResult[y, z] = 20
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    # cv2.resizeWindow('image', 1001, 1001)  
    # cv2.imshow('image', imgResult)
    # cv2.waitKey(1)  


start_time = time.time()
imgRadius = 500
image = cv2.imread('dad.jpg', cv2.IMREAD_GRAYSCALE)




height, width = image.shape[0:2]
minEdge= min(height, width)
topEdge = int((height - minEdge)/2)
leftEdge = int((width - minEdge)/2)
imgCropped = image[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]
kitty = cv2.resize(imgCropped, (2*imgRadius + 1, 2*imgRadius + 1)) 
cv2.imwrite('./resized.png', kitty)


#nrows, ncols = kitty.shape
# row, col = np.ogrid[:nrows, :ncols]
# cnt_row, cnt_col = nrows / 2, ncols / 2
# outer_disk_mask = ((row - cnt_row)**2 + (col - cnt_col)**2 >
#                        (nrows / 2)**2)
# kitty[outer_disk_mask] = 0
# print len(kitty[outer_disk_mask])
# print np.sum(kitty[outer_disk_mask])
# cv2.imwrite('testing.png', kitty)
# exit(0)


height, width = kitty.shape[:2]
imgResult = 255 * np.ones((height, width))
nLines = 1000
nPins = 200
oldPin = 0

x = int(width/2)
y = int(height/2)

coords = make_circle(center=(x,y),r=imgRadius, n=nPins)

# if you want less local lines
# for x in coords:
#     y,z = x
#     cv2.circle(kitty,(y,z), 55, (255,255,0), -1)


line_list = []

for line in range(nLines):
    bestLine = float("inf")
    oldCoord = coords[oldPin]

    for index in range(1, nPins):
        pin = (oldPin + index) % nPins
        pixels = 0
        coord = coords[pin]
        if check_tooclose(coords, oldPin, pin):
            continue
        bre = list(bresenham(oldCoord[0], oldCoord[1], coord[0], coord[1]))
        pixels = sum(kitty[x[0], x[1]] for x in bre)
        lineSum = int(pixels / len(bre)) 
        if lineSum < bestLine:
            bestLine = lineSum
            bestPin = pin
            bestBre = bre

    line_list.append((oldPin, bestPin))
    update_image(bestBre, kitty, imgResult)
    oldPin = bestPin

#v2.imwrite('john2.png', kitty)
cv2.imwrite('dadpixel2.png', imgResult)
# cv2.imshow('image', imgResult)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
print time.time() - start_time, "seconds"