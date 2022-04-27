import time
import math
import Adafruit_PCA9685

bot = 12
mid = 13
top = 14
gripper = 15

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

motor_pos = [530, 100, 450, 180]

def motor_kill():
    pwm = Adafruit_PCA9685.PCA9685()

def ang_to_pwm(angle):
    #   1 pwm = 0.45 degrees
    pwm_out = round(180/math.pi * angle/0.45)
    return pwm_out

def slow_move(motor, position):
    while position != motor_pos[motor - 12]:
        if abs(position - motor_pos[motor - 12]) < 5:
            motor_pos[motor - 12] = position
        elif position - motor_pos[motor - 12] < 0:
            motor_pos[motor - 12] -= 1
        else:
            motor_pos[motor - 12] += 1
        pwm.set_pwm(motor, 0, motor_pos[0])
        time.sleep(0.03)
        
        

def motor_default():
    pwm.set_pwm(bot, 0, motor_pos[0]) #perpendicular to robot
    pwm.set_pwm(mid, 0, motor_pos[1]) #perpendicular to arm one
    pwm.set_pwm(top, 0, motor_pos[2]) #flat to arm two
    pwm.set_pwm(gripper, 0, motor_pos[3]) #almost closed

def set_arm(a, b, c):
    #slow_move(bot, a)
    #slow_move(mid, b)
    #slow_move(top, 450)
    #slow_move(gripper, c)
    motor_default()
    time.sleep(0.5)
    pwm.set_pwm(bot, 0, a)
    pwm.set_pwm(mid, 0, b)
    pwm.set_pwm(top, 0, 450)
    pwm.set_pwm(gripper, 0, c)

def lcos(a, b, c):
    angle_a = math.acos((b**2 + c**2 - a**2) / (2*b*c)) #RETURNS ANGLE A
    return angle_a

def move_arm(y_pos, z_pos):
    print("MOVING")
    arm_1 = 6.5
    arm_2 = 11
    point_dis = math.sqrt(y_pos**2 + z_pos**2)
    if point_dis > arm_1 + arm_2:
        print("TOO FAR")
    else:
        angle_a = lcos(abs(z_pos), abs(y_pos), point_dis) - lcos(arm_2, arm_1, point_dis)
        angle_b = lcos(point_dis, arm_1, arm_2)
        if y_pos < 0:
            motor_a = ang_to_pwm(angle_a) + 120
            motor_b = ang_to_pwm(angle_b)
        elif y_pos > 0:
            motor_a = 520 - ang_to_pwm(angle_a)
            motor_b = 800 - ang_to_pwm(angle_b)
    if motor_a > 210:
        set_arm(motor_a, motor_b, 250)
    else:
        print("FAILED OUT OF RANGE")

#move_arm(4, 16)
#motor_default()
#time.sleep(1)
#slow_move(bot, 220)
#set_angles(230, 400, 230)
#set_arm(276, 354, 250)
#time.sleep(1)
#motor_kill()