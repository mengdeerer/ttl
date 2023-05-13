'''
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-13 20:50:38
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-13 20:51:01
FilePath: \tello\1.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
'''
from robomaster import robot
import robomaster

if __name__ == '__main__':
    # 如果本地IP 自动获取不正确，手动指定本地IP地址
    robomaster.config.LOCAL_IP_STR = "192.168.10.2"
    tl_drone = robot.Drone()
    # 初始化
    tl_drone.initialize()

    tl_flight=tl_drone.flight
    tl_flight.takeoff().wait_for_completed()
    tl_flight.forward(distance=50).wait_for_completed()
    tl_flight.backward(distance=50).wait_for_completed()
    tl_flight.land().wait_for_completed()
    
    
    tl_drone.close()