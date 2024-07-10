import cv2
import numpy as np

def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of colors in HSV
    colors = {
        "red": ((0, 100, 100), (180, 255, 255)),
        "green": ((36, 100, 100), (86, 255, 255)),
        "blue": ((100, 100, 100), (140, 255, 255)),
        "yellow": ((16, 100, 100), (36, 255, 255))
    }

    detected_colors = set()

    for color_name, (lower, upper) in colors.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                detected_colors.add(color_name)

    return frame, detected_colors

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    frame, detected_colors = detect_color(frame)

    cv2.imshow("Frame", frame)
    
    if detected_colors:
        print(f"Detected colors: {', '.join(detected_colors)}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
