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

# tl_flight.up(80).wait_for_completed()
i=0
tl_camera.start_video_stream(display=True)
while 1:
        num=input("请输入数字：")
        if int(num)==1:
                img = tl_camera.read_cv2_image()
                cv2.imwrite(f"./12/{i}.jpg", img)
                i+=1
                cv2.imshow("Drone", img)
                cv2.waitKey(1)
cv2.destroyAllWindows()
tl_camera.stop_video_stream()
tl_drone.close()
