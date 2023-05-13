from robomaster import camera
from robomaster import robot
import robomaster
import cv2
import time

tl_drone = robot.Drone()
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tl_drone.initialize()

tl_flight=tl_drone.flight
tl_camera= tl_drone.camera
# tl_flight.takeoff().wait_for_completed()
# tl_flight.forward(distance=50).wait_for_completed()
# tl_flight.up(80).wait_for_completed()

tl_camera.start_video_stream(display=False)
for i in range(0, 100):
    img = tl_camera.read_cv2_image(strategy='newest')
    cv2.imwrite(f"./pic/5/{i}.jpg",img)
    cv2.imshow("Drone", img)
    cv2.waitKey(1)
    time.sleep(0.5)
cv2.destroyAllWindows()
tl_camera.stop_video_stream()


# tl_flight.backward(distance=50).wait_for_completed()
# tl_flight.land().wait_for_completed()
    
tl_drone.close()
