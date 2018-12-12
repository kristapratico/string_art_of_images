import math
import numpy as np
import cv2
import time


# https://stackoverflow.com/questions/5186939/algorithm-for-drawing-a-4-connected-line
def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)    # distance to travel in X
    dy = abs(y1 - y0)    # distance to travel in Y

    if x0 < x1:
        ix = 1           # x will increase at each step
    else:
        ix = -1          # x will decrease at each step

    if y0 < y1:
        iy = 1           # y will increase at each step
    else:
        iy = -1          # y will decrease at each step

    e = 0                # Current error 

    for i in range(dx + dy):
        yield (x0, y0)
        e1 = e + dy
        e2 = e - dx
        if abs(e1) < abs(e2):
            # Error will be smaller moving on X
            x0 += ix
            e = e1
        else:
            # Error will be smaller moving on Y
            y0 += iy
            e = e2

def get_pin_pin_list(center=(0, 0), r=150, n=200):
    points = np.array([[int(center[0] + math.cos(np.pi*2*i/n) * r), int(center[1] + math.sin(np.pi*2*i/n) * r)] for i in range(n)])
    return points

def pins_too_close(pin_list, pinA, pinB):
    if abs(pinA - pinB) < 25:
        return True

def update_image(pinx, piny, kitty):
    mask = np.zeros(kitty.shape[:2], dtype = "uint8")
    cv2.line(mask, pinx, piny, 255, 1)
    cv2.line(imgResult, pinx, piny, 0, 1)
    kitty = cv2.bitwise_or(kitty, mask)
 
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    # cv2.resizeWindow('image', 1001, 1001)  
    # cv2.imshow('image', imgResult)
    # cv2.waitKey(1) 

    return kitty


start_time = time.time()
radius = 500 
image = cv2.imread('kk.jpg', cv2.IMREAD_GRAYSCALE)


height, width = image.shape[0:2]
minEdge= min(height, width)
topEdge = int((height - minEdge)/2)
leftEdge = int((width - minEdge)/2)
imgCropped = image[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]
kitty = cv2.resize(imgCropped, (2*radius + 1, 2*radius + 1)) 
cv2.imwrite('./resized.png', kitty)


height, width = kitty.shape[:2]
imgResult = 255 * np.ones((height, width))
num_lines = 1000
num_pins = 200
oldPin = 0

center_x = int(width/2)
center_y = int(height/2)

pin_list = get_pin_pin_list(center=(center_x,center_y),r=radius, n=num_pins)

line_list = []

for line in range(num_lines):
    bestLine = float("inf")
    oldCoord = pin_list[oldPin]

    for index in range(1, num_pins):
        pin = (oldPin + index) % num_pins
        coord = pin_list[pin]

        if pins_too_close(pin_list, oldPin, pin):
            continue

        line_pin_list = list(bresenham(oldCoord[0], oldCoord[1], coord[0], coord[1]))  
        pinX, pinY = zip(*line_pin_list)
        pixel_sum = np.sum(kitty[pinY, pinX])
        lineSum = int(pixel_sum / len(line_pin_list))
        if lineSum < bestLine:
            bestLine = lineSum
            bestPin = pin

    line_list.append((oldPin, bestPin))   
    kitty = update_image(tuple(pin_list[oldPin]), tuple(pin_list[bestPin]), kitty)
    oldPin = bestPin

cv2.imwrite('kkre.png', kitty)
cv2.imwrite('kk_results.png', imgResult)
# cv2.imshow('image', imgResult)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
print time.time() - start_time, "seconds"