"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-18 21:29:01
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-20 09:57:15
FilePath: \tello\cordinate.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
"""
Author: mengdeerer mengdeerer@gmail.com
Date: 2023-05-18 21:29:01
LastEditors: mengdeerer mengdeerer@gmail.com
LastEditTime: 2023-05-19 21:03:42
FilePath: \tello\cordinate.py
Description and Problems: 

Copyright (c) 2023 by mengdeerer, All Rights Reserved. 
"""
import cv2
import numpy as np
   

def pixel2camera(u, v, depth):
    # 将像素坐标转换为归一化坐标
    fx = 922.13825478
    cx = 481.19501769
    fy = 919.80817098
    cy = 351.71399502
    x = (u - cx) / fx
    y = (v - cy) / fy

    # 计算相机坐标
    Xc = x * depth

    Yc = y * depth
    Zc = depth
    return Zc, -Xc, -Yc


print(pixel2camera(200, 400, 300))
