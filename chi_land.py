import cv2
import numpy as np
from robomaster import camera
from robomaster import robot
import robomaster
cam_mat = np.array(
    [
        [921.23415725, 0.0, 490.14027498],
        [0.0, 919.74811543, 355.78729266],
        [0.0, 0.0, 1.0],
    ]
)
coef_mat = np.array([[0.01300172, -0.17542407, 0.00190941, -0.00171416, 0.55346324]])


def get_xyz(img, id_,long=28.5):
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()
    # 设了一个自适应阈值的参数，当时默认参数检测不出来，一般默认就行
    arucoParams.adaptiveThreshWinSizeStep = 1

    # 检测并可视化
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        img, arucoDict, parameters=arucoParams
    )
    cv2.aruco.drawDetectedMarkers(img, corners, ids)

    vec = []

    if corners == ():
        print("No aruco detected!")
        return img, vec

    for jdx, (marker, id) in enumerate(zip(corners, ids)):
        if id_ == id:
            print("jdx:{} \n marker:{} \n id:{}".format(jdx, marker, id))
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                marker, long, cam_mat, coef_mat
            )
            print("rvec:{} \n tvec:{}".format(rvec, tvec))
            vec = tvec
    return img, vec


if __name__ == "__main__":
    img=cv2.imread("./12/2.jpg")     
    _,tvec=get_xyz(img,3, 27)
    print("hhhhhh",tvec)