import cv2
import numpy as np
import math

# 定义红色的 HSV 范围
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])


def getCircle(img):
    # 已知参数
    KNOWN_WIDTH = 120  # 目标宽度为 15cm
    FOCAL_LENGTH = 858  # 摄像机焦距为 1000px

    # 加载图像
    image = img
    # 转换为 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 使用颜色过滤器获取红色区域
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 使用形态学操作去除噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 进行霍夫圆检测
    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        1,
        100,
        param1=100,
        param2=20,
        minRadius=0,
        maxRadius=0,
    )
    if circles is None:
        return -1, -1
    # 获取检测到的圆形列表中的第一个圆形
    circle = circles[0][0]

    # 绘制圆形
    center = (int(circle[0]), int(circle[1]))
    radius = int(circle[2])
    cv2.circle(image, center, radius, (0, 255, 0), 2)

    height, width, _ = image.shape

    # 计算像素宽度
    pixelWidth = circle[2] * 2

    # 计算距离
    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / pixelWidth
    print("Distance: {:.2f}cm".format(distance))

    # 计算像素长度
    pixelLength = center[0] - width / 2

    # 计算中心与图像中心的实际距离
    length = (distance * pixelLength) / FOCAL_LENGTH
    print("Length: {:.2f}cm".format(length))

    # 计算物体中心与图像中心之间的角度差
    angle_diff = math.asin(length / distance) * 180 / math.pi
    # 在图像中显示距离,物体中心和图像中心之间的实际距离和角度（+代表霍夫圆检测中心在图像右侧，-代表霍夫圆检测中心在图像左侧）
    cv2.putText(
        image,
        "{:.2f}cm".format(distance),
        (int(circle[0]), int(circle[1])),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        image,
        "{:.2f}cm".format(length),
        (int(circle[0]), int(circle[1]) + 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        image,
        "{:.2f}deg".format(angle_diff),
        (int(circle[0]), int(circle[1]) + 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    # 显示结果
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if  length>10 or length<-10:
        return 0,angle_diff
    else: return distance, angle_diff
