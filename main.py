"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-17 13:31:00
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-18 20:38:07
FilePath: \tello\main.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
from robomaster import robot
import robomaster
import cv2
import time
import finger_detect
import chi_land
import red

flag=0
c_times=0

tl_drone = robot.Drone()
robomaster.config.LOCAL_IP_STR = "192.168.10.2"
tl_drone.initialize()
tl_flight = tl_drone.flight

tl_camera = tl_drone.camera
tl_camera.start_video_stream(display=False)
tl_camera.set_resolution("high")
tl_camera.set_bitrate(6)


def getImage():
    array1 = []
    arrayL = []
    countL = 0
    countR = 0
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(0, 50):
        img = tl_camera.read_cv2_image(strategy="newest")
        lor, num, img1 = finger_detect.all_in_one(img.copy())
        arrayL.append(lor)
        array1.append(num)
        cv2.imshow("Drone", img1)
        cv2.imwrite("./test/finger.jpg", img1)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(0, 50):
        if arrayL[i] == "Left":
            countL += 1
        if arrayL[i] == "Right":
            countR += 1
        if array1[i] == 1:
            count1 += 1
        if array1[i] == 2:
            count2 += 1
        if array1[i] == 3:
            count3 += 1
    if countL > countR:
        hand = "Left"
    else:
        hand = "Right"
    if count1 > count2 and count1 > count3:
        number = 1
    if count2 > count1 and count2 > count3:
        number = 2
    if count3 > count1 and count3 > count2:
        number = 3
    return hand, number


def getAruco(id,long=28.5):
    tvec = []
    while tvec==[]:
        global flag
        flag+=1
        img = tl_camera.read_cv2_image(strategy="newest")
        img_v, tvec = chi_land.get_xyz(img.copy(), id,long)
        cv2.imshow("Drone", img_v)
        cv2.imwrite(f"./test/aruco1{flag}.jpg", img_v)
    print(tvec)
    x = tvec[0][0][0]
    y = tvec[0][0][1]
    z = tvec[0][0][2]
    x, y, z = change(x, y, z)
    return x, y, z


def change(x, y, z):
    return int(z), int(-x), int(-y)



def fly(x, y):
    if(x>=500):
        xx=int(x/2)
        yy=int(y/2)
        tl_flight.go(xx, yy, 0, 70).wait_for_completed()
        tl_flight.go(xx, yy, 0, 70).wait_for_completed()
    else:tl_flight.go(x, y, 0, 70).wait_for_completed()

     
    

tl_flight.takeoff().wait_for_completed()
tl_flight.up(80).wait_for_completed()
rol, num = getImage()
print(rol, num)
height = 0


if rol == "Right":
    tl_flight.left(60).wait_for_completed()
    x, y, z = getAruco(10)
    fly(x+40,y)
    # tl_flight.left(120).wait_for_completed()
    tl_flight.go(60,-100,0,70).wait_for_completed()
else:
    tl_flight.right(60).wait_for_completed()
    x, y, z = getAruco(20)
    fly(x+40,y)
    tl_flight.go(60,100,0,70).wait_for_completed()

x, y, z = getAruco(30)
if x>420 or x<100:
    fly(370,0)
else:fly(x+10,y)

tl_flight.left(260).wait_for_completed()
tl_flight.rotate(angle=40, retry=True).wait_for_completed()
# img=tl_camera.read_cv2_image(strategy="newest")
# cv2.imwrite(f"./test/red{flag}.jpg", img)
# flag+=1
# dis,angel=red.getCircle(img)
# tl_flight.rotate(angle=angel, retry=True).wait_for_completed()
# while dis==0 or dis==-1:
#     if(angel>6):
#         fly(-30,-20)
#     if(angel<-6):
#         fly(-30,20)
#     img=tl_camera.read_cv2_image(strategy="newest")
#     dis,angel=red.getCircle(img)
#     cv2.imwrite(f"./test/red{flag}.jpg", img)
#     flag+=1
#     tl_flight.rotate(angle=angel, retry=True).wait_for_completed()
#     c_times+=1
#     if(c_times>=5):
#         dis=270
#         break
#     if(dis>350):
#         dis=270
#         break
dis=350
fly(dis,0)

tl_flight.rotate(angle=35, retry=True).wait_for_completed()

tl_flight.left(150).wait_for_completed()


tl_flight.down(40).wait_for_completed()

x, y, z = getAruco(num,27)
fly(x,y)

tl_camera.stop_video_stream()
tl_flight.land().wait_for_completed()
tl_drone.close()
