# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os

directory = "dataTest"
test_label_cat = os.listdir(directory)
test_images_path = []
name = []
for cat in test_label_cat:
    for image in os.listdir(directory+"/"+cat):
        test_images_path.append(directory+"/"+cat+"/"+image)
        name.append(image[0])
clf = joblib.load("test_ppc4_cpb5.pkl")
score = 0
maxscore = len(name)
for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(4,4), cells_per_block=(5,5), visualize=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    nb = str(nbr)
    if (nb[3] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")
print("Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))