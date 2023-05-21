import cv2
import numpy as np

# 读入图片
img = cv2.imread('aa.jpg')
# 读取 Aruco 字典
# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
}
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_50"])
# 初始化 Aruco 检测器
arucoParams = cv2.aruco.DetectorParameters()
# 检测 Aruco 码
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
print(corners)
print(ids)