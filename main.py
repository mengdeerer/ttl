from robomaster import robot
import robomaster
import cv2
import time
import finger_detect


tl_drone = robot.Drone()
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tl_drone.initialize()
tl_flight = tl_drone.flight

tl_camera = tl_drone.camera

tl_camera.start_video_stream(display=False)


def getImageRol():
    # time.sleep(1)phu
    array1 = []
    countL = 0
    countR = 0
    for i in range(0, 100):
        img = tl_camera.read_cv2_image(strategy="newest")
        lor, img1 = finger_detect.left_or_right(img.copy())
        array1.append(lor)
        cv2.imshow("Drone", img1)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    # tl_camera.stop_video_stream().wait_for_completed()
    for i in range(0, 20):
        if array1[i] == "Left":
            countL += 1
        if array1[i] == "Right":
            countR += 1
    if countL > countR:
        return "Left"
    else:
        return "Right"


def getFinger():
    # tl_camera.start_video_stream(display=False).wait_for_completed()
    # time.sleep(1)
    array = []
    for i in range(0, 100):
        img = tl_camera.read_cv2_image(strategy="newest")
        num, img2 = finger_detect.finger_count(img.copy())
        array.append(num)
        cv2.imshow("Drone", img2)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    # tl_camera.stop_video_stream()
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(0, 20):
        if array[i] == 1:
            count1 += 1
        if array[i] == 2:
            count2 += 1
        if array[i] == 3:
            count3 += 1
    if count1 > count2 and count1 > count3:
        return 1
    if count2 > count1 and count2 > count3:
        return 2
    if count3 > count1 and count3 > count2:
        return 3


# tl_flight.takeoff().wait_for_completed()
# tl_flight.up(120).wait_for_completed()
rol = getImageRol()
num = getFinger()
print(rol, num)

tl_camera.stop_video_stream()
# tl_flight.land().wait_for_completed()
tl_drone.close()
