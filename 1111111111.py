import cv2
import numpy as np


def get_xyz(img, id):

    pass


cam_mat = np.array([[921.23415725, 0.,         482.14027498],
                    [0.,        919.74811543, 353.78729266],
                    [0.,           0.,           1.]])
coef_mat = np.array(
    [[0.01300172, -0.17542407, 0.00190941, -0.00171416,  0.55346324]])

if __name__ == '__main__':

    frame = cv2.imread('./3/4.png')
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters()
    # 设了一个自适应阈值的参数，当时默认参数检测不出来，一般默认就行
    arucoParams.adaptiveThreshWinSizeStep = 1

    # 检测并可视化
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict,
                                                       parameters=arucoParams)
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    for jdx, marker in enumerate(corners):

        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            marker, 27, cam_mat, coef_mat)
        print("rvec:{} \n tvec:{}".format(rvec, tvec))
        # cv2.aruco.drawAxis(frame, cam_mat, coef_mat, rvec, tvec, 1)

    cv2.imshow("233", frame)
    key = cv2.waitKey()
