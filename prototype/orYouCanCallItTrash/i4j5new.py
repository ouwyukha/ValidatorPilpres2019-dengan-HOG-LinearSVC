# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os

directory = "mid_data/dataset_splitted"
SizeDir = os.listdir(directory)
test_label_list = os.listdir(directory)
test_images_path = []
name = []

for size in SizeDir:
    catdir = os.listdir(directory+"/"+size)
    for cat in catdir:
        files = os.listdir(directory+"/"+size+"/"+cat)
        for file in files:
            test_images_path.append(directory+"/"+size+"/"+cat+"/"+file)
            name.append(file[0])
            
clf = joblib.load("beta_test_ppc4_cpb5_new.pkl")
score = 0
maxscore = len(name)
for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    #(y,x) 77 40
    if image.shape[0] == 34 and image.shape[1] == 37:
        image = cv2.resize(image,(77,40))
    roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(4, 4), cells_per_block=(5, 5), visualize=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    nb = str(nbr)
    if (nb[3] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")
print("Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))