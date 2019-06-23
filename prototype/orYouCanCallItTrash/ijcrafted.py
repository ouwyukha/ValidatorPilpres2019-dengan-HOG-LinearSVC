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

ppc=7
cpb=7
tuple_ppc=(7,7)
tuple_cpb=(7,7)

for size in SizeDir:
    catdir = os.listdir(directory+"/"+size)
    for cat in catdir:
        files = os.listdir(directory+"/"+size+"/"+cat)
        for file in files:
            test_images_path.append(directory+"/"+size+"/"+cat+"/"+file)
            name.append(file[0])
            
clf = joblib.load("crafted_ppc"+str(ppc)+"_cpb"+str(cpb)+"_new.pkl")
score = 0
maxscore = len(name)
for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    image = cv2.resize(image,(98,49))
    roi_hog_fd = hog(image, orientations=9, pixels_per_cell=tuple_ppc, cells_per_block=tuple_cpb, visualize=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    nb = str(nbr)
    if (nb[3] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")
print(str(ppc)+","+str(cpb)+" :\tScore : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))