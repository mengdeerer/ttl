"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-18 23:41:59
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-19 21:45:12
FilePath: \tello\arr.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
import cv2
import numpy as np
import math


# camera_matrix = None
# dist_coeffs = None

# camera_matrix = np.array(
#     [[922.13825478, 0, 481.19501769], [0, 919.80817098, 351.71399502], [0, 0, 1]],
#     dtype="float32",
# )

# # 畸变系数
# dist_coeffs = np.array([0, 0, 0, 0], dtype="float32")
# # 定义aruco字典
# aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# # 定义aruco探测器参数
# parameters =  aruco.DetectorParameters_create()

# # 读取输入图像
img = cv2.imread("aa.jpg")
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
}
aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_50"])
parameters = cv2.aruco.DetectorParameters()
# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# size=gray.size[::-1]
size = gray.shape[::-1]
# 检测所有aruco码
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
    gray, aruco_dict, parameters=parameters
)

objp=np.zeros((2*2,3),np.float32)
objp[:,:2]=np.mgrid[0:2,0:2].T.reshape(-1,2)
objp=objp*0.10
img_points=[]
obj_points=[[[ 0. ,  0. ,  0. ],[ 0.1 ,  0. ,  0. ],[0.,0.1,0.],[0.1,0.1,0.]]]
obj_points.append(objp)
if ids is not None and len(ids) > 0:
    # 计算 Aruco 码姿态估计
    obj_points.append(objp[0])
    img_points.append(corners[0])
    print(obj_points)
    print(img_points)
_, mtx, dist, _, _ = cv2.calibrateCamera(obj_points, img_points, size, None, None)


Camera_intrinsic = {
    "mtx": mtx,
    "dist": dist,
}