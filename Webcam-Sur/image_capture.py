from cv2 import *

cam = VideoCapture(0)
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test", WINDOW_AUTOSIZE)
    imshow("cam-test",img)
    destroyWindow("cam-test")
    imwrite("test.jpg",img) 