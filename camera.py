"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-13 21:13:03
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-13 23:23:02
FilePath: \tello\camera.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
from robomaster import camera
from robomaster import robot
import robomaster
import cv2
import time

tl_drone = robot.Drone()
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tl_drone.initialize()

tl_flight = tl_drone.flight
tl_camera = tl_drone.camera
# tl_flight.takeoff().wait_for_completed()
# tl_flight.forward(distance=50).wait_for_completed()
# tl_flight.up(80).wait_for_completed()

tl_camera.start_video_stream(display=False)
for i in range(0, 1000):
    img = tl_camera.read_cv2_image()
    cv2.imwrite(f"./1/{i}.jpg", img)
    cv2.imshow("Drone", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()
tl_camera.stop_video_stream()


# tl_flight.backward(distance=50).wait_for_completed()
# tl_flight.land().wait_for_completed()

tl_drone.close()
