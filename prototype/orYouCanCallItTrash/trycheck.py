# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os

directory = "dataTest"
test_label_list = os.listdir(directory)
test_images_path = []
name = []
for image in test_label_list:
    test_images_path.append(directory+"/"+image)
    name.append(image[0])
clf = joblib.load("trycreate.pkl")
score = 0
maxscore = len(test_label_list)
for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(4,4), cells_per_block=(5,5), visualize=False)
    scoreTable = np.matmul(clf,np.array(roi_hog_fd, 'float64'))
    asd = len(scoreTable)
    maxindexscore = -1
    maxindex = -1
    for i in range(asd):
        if scoreTable[i] > maxindexscore:
            maxindex = i
            maxindexscore = scoreTable[i]
    
    Classy = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'X':10}

    nb = str(Classy[str(maxindex)])
    if (nb == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")
print("Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))