import cv2
import numpy as np

# 相机内参
camera_matrix = np.array([[1200, 0, 500], [0, 1200, 500], [0, 0, 1]])

# 畸变系数
distortion_coef = np.array([0.1, 0.01, -0.001, 0.0025])

# 相机外参
rvec = np.array([0.1, 0.2, 0.3])
tvec = np.array([0.5, 0.5, 1])

# 像素坐标
pixel_point = np.array([300, 400])

# 像素坐标转换为归一化平面坐标
normalized_plane_point = cv2.undistortPoints(np.array([pixel_point]), camera_matrix, distortion_coef, None, camera_matrix)

# 归一化平面坐标转换为相机坐标
rotation_matrix, _ = cv2.Rodrigues(rvec)  # 旋转向量转换为旋转矩阵
camera_point = np.dot(np.linalg.inv(rotation_matrix), normalized_plane_point[0] - tvec)

print(camera_point)