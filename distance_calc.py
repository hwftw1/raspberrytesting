import math

def deg_to_rad(degrees):
  radians = degrees * math.pi/180
  return radians

def get_distance(left_cords, right_cords, cam_distance = 12.5):
    
    #depth calculation
    c = cam_distance
    if left_cords[0] > 0.5:
        angle_b = left_cords[0] - 0.5
        angle_b = angle_b * (70.42)
        angle_b = 90 - angle_b
    elif left_cords[0] < 0.5:
        angle_b = left_cords[0]
        angle_b = angle_b * (70.42)
        angle_b = 180 - angle_b
    if right_cords[0] < 0.5:
        angle_a = right_cords[0] * 53.5
        angle_a = 53.5/2 - angle_a
        angle_a = 90 - angle_a
    elif right_cords[0] > 0.5:
        angle_a = right_cords[0] - 0.5
        angle_a = right_cords[0] * 53.5
        angle_a = angle_a + 90
    angle_c = 180 - (angle_b + angle_a)
    a = c * math.sin(deg_to_rad(angle_a)) / math.sin(deg_to_rad(angle_c))
    depth = a * math.sin(deg_to_rad(angle_b))
  
    #x position in relation to raspicam
    if angle_a >= 90:
        x_hypo = depth / math.sin(deg_to_rad(angle_a))
        dist_x = math.sqrt(x_hypo*x_hypo - depth*depth)
    elif angle_a < 90:
        x_hypo = depth / math.sin(deg_to_rad(angle_a))
        dist_x = math.sqrt(x_hypo*x_hypo - depth*depth)
        dist_x = dist_x * -1
    #y position in relation to raspicam
    if right_cords[1]  > 0.5:
        angle_y = (right_cords[1] - 0.5)
        angle_y = 90 - angle_y * 41.41
        y_hypo = depth / (math.sin(deg_to_rad(angle_y)))
        dist_y = math.sqrt(y_hypo*y_hypo - depth*depth)
        dist_y = dist_y * -1
    elif right_cords[1] < 0.5:
        angle_y = right_cords[1]
        41.1 - angle_y * 41.1
        angle_y = 90 - angle_y
        y_hypo = depth / (math.sin(deg_to_rad(angle_y)))
        dist_y = math.sqrt(y_hypo*y_hypo - depth*depth)
    
    return depth, dist_x, dist_y

#test values, should return 23.473, 3.036, 4.135
# left = [0.7661458333333333, 0.7768518518518519]
# right = [0.36226851851851855, 0.7412551440329218]
# print(get_distance(left, right))
