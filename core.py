import cv2
import numpy as np
img=cv2.imread('Files/img.png')
core = np.array([  [-1.0, -1.0, -1.0],
                   [-1.0,  9.0, -1.0],
                   [-1.0, -1.0, -1.0]])
core=core

res=cv2.filter2D(img,-1,core)
cv2.imshow("res",res)
cv2.waitKey(0)