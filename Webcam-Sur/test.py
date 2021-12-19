# Importing all necessary libraries
import cv2
import os

name = "recordings\\18-12-2021-22-39-11.mp4"
cam = cv2.VideoCapture(os.path.join(os.path.abspath(os.path.dirname(__file__)), name))

count = 0
currentframe = 0
maxframe = 5
multiplier = 2 # default frame skips between each image

length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

if length > 20:
    multiplier = int(length / 5)
    print(f"With video frames of {length}, the frame multiplier has been set to {multiplier}")

while(True):
    ret, frame = cam.read()
    if ret and count % 50 == 0:
        name = f'image-capture({int(currentframe / multiplier)}).jpg'
        cv2.imwrite(name, frame)
        currentframe += multiplier
        count += 1

        if count == 100:
            break
    else:
        count += 1

cam.release()
cv2.destroyAllWindows()