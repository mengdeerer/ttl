import chi_land
import cv2
import numpy as np

img=cv2.imread("2/2.png")
_,vec=chi_land.get_xyz(img,30)
print("hh",vec[0][0][2])