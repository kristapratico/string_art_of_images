import math
from math import pi
import numpy as np
import cv2
from bresenham import bresenham



imgRadius = 500 
image = cv2.imread('kitty.png', cv2.IMREAD_GRAYSCALE)
height, width = image.shape[0:2]
minEdge= min(height, width)
topEdge = int((height - minEdge)/2)
leftEdge = int((width - minEdge)/2)
imgCropped = image[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]
kitty = cv2.resize(imgCropped, (2*imgRadius + 1, 2*imgRadius + 1)) 
cv2.imwrite('./resized.png', kitty)

height, width = kitty.shape[:2]
previousPins = []
imgResult = 255 * np.ones((height, width))
nLines = 700
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

# def line_drawn(coords, line, adj):
#     checkme = line, adj
#     if checkme in coords:
#         return True

coords = make_circle(center=(x,y),r=500)

# for x in coords:
#     y,z = x
#     cv2.circle(kitty,(y,z), 65, (255,0,0), -1)
# for line in coords:
#     sumpix = list()
#     for adj in coords:
#         if check_tooclose(line, adj):
#             continue
#         bre = list(bresenham(line[0], line[1], adj[0], adj[1]))
#         for x in bre:
#             y, z = x
#             pixels = list()
#             if y < height and z < width:
#                 pixels.append(int(kitty[y, z]))
#         sumpix.append(int(np.sum(pixels)/len(bre)))

#     if sumpix:
#         themin = sumpix.index(min(sumpix))
#         kitty = cv2.line(kitty, tuple(line), tuple(coords[themin]), (255,255,255), 1)
#         #im = cv2.line(im, tuple(line), tuple(coords[themin]), 15, 1)

# cv2.imwrite('lol.png', kitty)
line_list = []
    # Loop over lines until stopping criteria is reached
for line in range(nLines):
    bestLine = 9999999999
    oldCoord = coords[oldPin]

    # Loop over possible lines
    for index in range(1, nPins):
        pin = (oldPin + index) % nPins
        pixels = 0
        coord = coords[pin]
        if check_tooclose(coords, oldPin, pin):
            continue
        bre = list(bresenham(oldCoord[0], oldCoord[1], coord[0], coord[1]))
        for x in bre:
            y, z = x
            pixels += int(kitty[y, z])
        lineSum = int(pixels / len(bre)) 
        if lineSum < bestLine:
            bestLine = lineSum
            bestPin = pin
            bestBre = bre

    line_list.append((oldPin, bestPin))
    for x in bestBre:
        y, z = x
        kitty[y, z] = 255
        imgResult[y, z] = 0

    if bestPin == oldPin:
        print "hi"
        break


    oldPin = bestPin

cv2.imwrite('lol6.png', kitty)
cv2.imwrite('threaded6.png', imgResult)