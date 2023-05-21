"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-18 20:45:51
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-20 16:03:11
FilePath: \tello\aruco.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-18 20:45:51
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-19 21:35:02
FilePath: \tello\aruco.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
# detect_aruco_image.py
#   用法
# python detect_aruco_image.py --image images/example_01.png --type DICT_5X5_100
# 导入库
import imutils
import cv2


def detect_aruco(img):
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    }
    print("[INFO] Loading image...")
    image = img
    arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_50"])
    arucoParams = cv2.aruco.DetectorParameters()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        image, arucoDict, parameters=arucoParams
    )
    print(len(corners))
    # 验证至少一个 ArUCo 标记被检测到
    if len(corners) > 0:
        # 展平 ArUCo ID 列表
        ids = ids.flatten()
        # 循环检测到的 ArUCo 标记
        for markerCorner, markerID in zip(corners, ids):
            # 从图像中得到的数字
            print("[INFO] ArUco marker ID: {}".format(markerID))
            # 提取始终按​​以下顺序返回的标记：
            # TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM-LEFT
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # 将每个 (x, y) 坐标对转换为整数
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # 绘制ArUCo检测的边界框
            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
            # 计算并绘制 ArUCo 标记的中心 (x, y) 坐标
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            # 在图像上绘制 ArUco 标记 ID
            cv2.putText(
                image,
                str(markerID),
                (topLeft[0], topLeft[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
        print(cX, cY, str(markerID))
        return str(markerID), cX, cY


if __name__ == "__main__":
    detect_aruco(cv2.imread("aaa.jpg"))
