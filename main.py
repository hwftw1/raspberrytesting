from camera import *
from arm_motion import *
from distance_calc import *
from move_bot import *

import torch
from PIL import Image
import cv2

def get_strawbs(img_input, img_size = 640):
    img_batch = []
    img = cv2.imread(img_input)
    img = cv2.resize(img, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_batch.append(img)
    results = model(img_batch, size=img_size)
    results.save()
    try:
        return [results.xywhn[0][0][0], results.xywhn[0][0][1]]
    except IndexError:
        return False

def make_space():
        # Image cleanup for new images
    if os.path.exists("runs/detect/exp/image0.jpg"):
        os.remove("runs/detect/exp/image0.jpg")
    if os.path.exists("runs/detect/exp2/image0.jpg"):
        os.remove("runs/detect/exp2/image0.jpg")
    if os.path.exists("runs/detect/exp/"):
        os.rmdir("runs/detect/exp/")
    if os.path.exists("runs/detect/exp2/"):
        os.rmdir("runs/detect/exp2/")
        
if __name__ == '__main__':
    #motor_kill()
    #destroy()
    #release_cam()
    print("-----SETUP-----")
    motor_default()
    model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')  # local repo
    model.conf = 0.8

    while(1):
        try:
            print("CYCLING")
            make_space()
            move(speed_set, 'forward', 'no', 0.8)
            time.sleep(0.25)
            motorStop()
            get_right()
            right_out = (get_strawbs("right.jpg"))
            if right_out != False:
                if right_out[0] <= 0.3:
                    print("-----TAKING PICTURES-----")
                    get_left()
                    left_out = (get_strawbs("left.jpg"))
                    print(left_out, right_out)
    #                 print("-----IDENTIFYING STRAWBERRIES (RIGHT)-----")
    #                 right_out = (get_strawbs("right.jpg"))
                    z, x, y = (get_distance(left_out, right_out))
                    move_arm(y, z)
        except KeyboardInterrupt:
            destroy()
            motor_kill()
            release_cam()
            break