import joblib
from skimage.feature import hog
import numpy as np
import cv2

feature = cv2.imread("tst.jpg",0)
fd = hog(feature, orientations=9, pixels_per_cell=(4, 4), cells_per_block=(5, 5), visualize=False)
for i in fd:
    print(i)
print(len(fd))
input()