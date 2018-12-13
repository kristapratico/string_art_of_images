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

def get_pin_list(center=(0, 0), r=150, n=200):
    points = np.array([[int(center[0] + math.cos(np.pi*2*i/n) * r), int(center[1] + math.sin(np.pi*2*i/n) * r)] for i in range(n)])
    return points

def pins_too_close(pinA, pinB):
    if abs(pinA - pinB) < 25:
        return True

def show_image(string_art, thread_count, num_lines):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
    cv2.resizeWindow('image', 1001, 1001)
    cv2.putText(string_art, str(thread_count - 1), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv2.putText(string_art, str(thread_count), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)  
    if thread_count == num_lines:
        cv2.putText(string_art, str(thread_count), (900, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv2.imshow('image', string_art)
    cv2.waitKey(1) 

def update_image(pinx, piny, image):
    mask = np.zeros(image.shape[:2], dtype = "uint8")
    cv2.line(mask, pinx, piny, 255, 1)
    cv2.line(string_art, pinx, piny, 0, 1)
    image = cv2.bitwise_or(image, mask)

    return image # do i need this?


start_time = time.time()

orig_img = cv2.imread('kk.jpg', cv2.IMREAD_GRAYSCALE)

radius = 500 
height, width = orig_img.shape[0:2]
minEdge= min(height, width)
topEdge = int((height - minEdge)/2)
leftEdge = int((width - minEdge)/2)
crop_img = orig_img[topEdge:topEdge+minEdge, leftEdge:leftEdge+minEdge]
image = cv2.resize(crop_img, (2*radius + 1, 2*radius + 1)) 


height, width = image.shape[:2]
string_art = 255 * np.ones((height, width))
num_lines = 1000
num_pins = 200
start_pin = 0

center_x = int(width/2)
center_y = int(height/2)

pin_list = get_pin_list(center=(center_x,center_y),r=radius, n=num_pins)

print_list = []
thread_count = 0

for line in range(num_lines):
    best_line = float("inf")
    start_coords = pin_list[start_pin]

    for pin in range(1, num_pins):
        end_pin = (start_pin + pin) % num_pins
        end_coords = pin_list[end_pin]

        if pins_too_close(start_pin, end_pin):
            continue

        line_coords = list(bresenham(start_coords[0], start_coords[1], end_coords[0], end_coords[1]))  
        pinX, pinY = zip(*line_coords)
        pixel_sum = np.sum(image[pinY, pinX])
        line_avg = int(pixel_sum / len(line_coords))
        if line_avg < best_line:
            best_pin = end_pin
            best_line = line_avg
            
    thread_count += 1
    print_list.append((start_pin, best_pin))   
    image = update_image(tuple(pin_list[start_pin]), tuple(pin_list[best_pin]), image)
    #show_image(string_art, thread_count, num_lines)
    start_pin = best_pin

cv2.imwrite('kk_results3.png', string_art)
cv2.namedWindow('image', cv2.WINDOW_NORMAL) 
cv2.resizeWindow('image', height, width)
cv2.imshow('image', string_art)
cv2.waitKey(0)
cv2.destroyAllWindows()
print int(time.time() - start_time), "seconds elapsed"
# write_file = open("instructions.txt", "w")
# write_file.writelines(str(print_list))