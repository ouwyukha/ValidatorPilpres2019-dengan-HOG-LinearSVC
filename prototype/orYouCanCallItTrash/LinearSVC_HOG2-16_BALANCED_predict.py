import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os

directory = "dataTest32"
test_label_list = os.listdir(directory)
test_images_path = []
name = []
for image in test_label_list:
    test_images_path.append(directory+"/"+image)
    name.append(image[0])
print("image added")
sizeDir = None
datdir = None
imdir = None
image = None

clf = joblib.load("LinearSVC_HOG2-16_CLF.pkl")

#clf = joblib.load("hogBalanced_ppc2_cpb16.pkl")

score = 0
maxscore = len(test_images_path)

for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(2,2), cells_per_block=(16,16), visualize=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    nb = str(nbr)
    if (nb[2] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")

print("2_16 - Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))