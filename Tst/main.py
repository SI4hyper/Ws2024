import cv2
import numpy as np
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
import digitalio

url = 'http://192.168.128.9:8000/video_feed'
cap = cv2.VideoCapture(url)

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x25)

portb = [mcp.get_pin(i + 8) for i in range(2)]
for pin in portb:
    pin.direction = digitalio.Direction.OUTPUT

sw1 = mcp.get_pin(0)
sw1.direction = digitalio.Direction.INPUT
sw1.pull = digitalio.Pull.UP

def led(values):
    for i in range(2):
        portb[i].value = values[i]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    center_x, center_y = width // 2, height // 2

    crop_size = 900
    crop_x1 = center_x - crop_size // 7
    crop_y1 = center_y - crop_size // 10
    crop_x2 = center_x + crop_size // 7
    crop_y2 = center_y + crop_size // 10

    cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

    hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
   # blurred = cv2.GaussianBlur(mask, (1, 1), 0)
   # karnel = np.ones((1, 1), np.uint8)
   # mask = cv2.erode(blurred, karnel, iterations=1)
   # mask = cv2.dilate(mask, karnel, iterations=1)

    result = cv2.bitwise_and(cropped_frame, cropped_frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detected_shapes = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(cropped_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if len(approx) == 3:
                shape_name = "Triangle"
            elif len(approx) == 4:
                    shape_name = "Square"
            elif len(approx) > 1:
                shape_name = "Circle"
            else:
                shape_name = "Unknown"
                
            cv2.putText(cropped_frame, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            detected_shapes.append(shape_name)
            
    cv2.rectangle(frame, (crop_x1, crop_y1), (crop_x2, crop_y2), (0, 0, 255), 2)

    cv2.imshow('Frame', frame)
   # cv2.imshow('Cropped Frame with Contours', cropped_frame)
    cv2.imshow('Mask', mask)
   # cv2.imshow('Result', result)

    if sw1.value:
        led.value = True
    else:
        if "Square" in detected_shapes and "Circle" in detected_shapes:
            led([False, True])
        elif "Square" in detected_shapes and "Triangle" in detected_shapes:
            led([True, False])
        elif "Circle" in detected_shapes and "Triangle" in detected_shapes:
            led([False, False])
        else:
            led([True, True])

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
