import cv2
import numpy as np
import math

# 定义红色的 HSV 范围
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

# 已知参数
KNOWN_WIDTH = 0.66 # 目标宽度为 15cm
FOCAL_LENGTH = 200000 # 摄像机焦距为 1000px

# 加载图像
image = cv2.imread("D:\pythonFiles\picture11.jpg")
# 转换为 HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 使用颜色过滤器获取红色区域
mask1 = cv2.inRange(hsv, lower_red, upper_red)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 + mask2

# 使用形态学操作去除噪声
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# 进行霍夫圆检测
circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=20, minRadius=0, maxRadius=0)

# 获取检测到的圆形列表中的第一个圆形
circle = circles[0][0]

# 绘制圆形
center = (int(circle[0]), int(circle[1]))
radius = int(circle[2])
cv2.circle(image, center, radius, (0, 255, 0), 2)


# 估算物体中心
center = (int(circle[0]), int(circle[1]))

# 计算物体中心与图像中心之间的角度差
height, width, _ = image.shape
angle_diff = math.atan2(width/2 - center[0], height/2 - center[1]) * 180 / math.pi

# 计算像素宽度
pixelWidth = circle[2] * 2

# 计算距离
distance = (KNOWN_WIDTH * FOCAL_LENGTH) / pixelWidth
print("Distance: {:.2f}cm".format(distance))

# 在图像中显示距离和角度
cv2.putText(image, "{:.2f}cm".format(distance), (int(circle[0]), int(circle[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(image, "{:.2f}deg".format(angle_diff), (int(circle[0]), int(circle[1])+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# 显示结果
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
