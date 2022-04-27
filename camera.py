import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 1920)
cam.set(4, 1080)

def get_pictures():
    get_right()
    get_left()

def get_right():
    os.system("libcamera-still -t 1 --nopreview -o /home/hwickens/code/right.jpg")
    
def get_left():
    ret, frame = cam.read()
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite('/home/hwickens/code/left.jpg', frame)
    
def release_cam():
    cam.release()

#get_pictures()
#release_cam()