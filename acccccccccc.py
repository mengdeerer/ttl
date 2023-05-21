import cv2
import numpy as np
import glob
import math


img = cv2.imread("aa.jpg")
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
}
aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_50"])
parameters = cv2.aruco.DetectorParameters()
# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
size=gray.size[::-1]
# 检测所有aruco码
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
    gray, aruco_dict, parameters=parameters
)

objp = np.zeros((6 * 9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
objp = 2.15 * objp  # 打印棋盘格一格的边长为2.6cm
obj_points = []  # 存储3D点
img_points = []  # 存储2D点
images = glob.glob("./biao/*.png")  # 黑白棋盘的图片路径

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = gray.shape[::-1]
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    print(corners)
    if ret:
        obj_points.append(objp)
        corners2 = cv2.cornerSubPix(
            gray,
            corners,
            (5, 5),
            (-1, -1),
            (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001),
        )
        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)
        cv2.drawChessboardCorners(img, (9, 6), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
_, mtx, dist, _, _ = cv2.calibrateCamera(obj_points, img_points, size, None, None)
# 内参数矩阵
Camera_intrinsic = {
    "mtx": mtx,
    "dist": dist,
}


obj_points = objp  # 存储3D点
img_points = []  # 存储2D点

# 从摄像头获取视频图像
# camera = cv2.VideoCapture(0)

while True:
    frame = cv2.imread("./biao/3.png")
    # _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    size = gray.shape[::-1]
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    if ret:  # 画面中有棋盘格
        img_points = np.array(corners)
        cv2.drawChessboardCorners(frame, (9, 6), corners, ret)
        # rvec: 旋转向量 tvec: 平移向量
        _, rvec, tvec = cv2.solvePnP(
            obj_points, img_points, Camera_intrinsic["mtx"], Camera_intrinsic["dist"]
        )  # 解算位姿
        distance = math.sqrt(tvec[0] ** 2 + tvec[1] ** 2 + tvec[2] ** 2)  # 计算距离
        rvec_matrix = cv2.Rodrigues(rvec)[0]  # 旋转向量->旋转矩阵
        proj_matrix = np.hstack((rvec_matrix, tvec))  # hstack: 水平合并
        eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角
        pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
        cv2.putText(
            frame,
            "dist: %.2fcm, yaw: %.2f, pitch: %.2f, roll: %.2f"
            % (distance, yaw, pitch, roll),
            (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
            break
    else:  # 画面中没有棋盘格
        cv2.putText(
            frame,
            "Unable to Detect Chessboard",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 0, 255),
            3,
        )
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
            break
print(rvec, tvec)
cv2.destroyAllWindows()
