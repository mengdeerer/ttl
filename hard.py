from robomaster import robot
import robomaster
import cv2
import time
import finger_detect
import aruco

tl_drone = robot.Drone()
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tl_drone.initialize()
tl_flight = tl_drone.flight

tl_flight.takeoff().wait_for_completed()
tl_flight.go(x=30, y=0, z=30, speed=10).wait_for_completed()


tl_flight.land().wait_for_completed()
tl_drone.close()