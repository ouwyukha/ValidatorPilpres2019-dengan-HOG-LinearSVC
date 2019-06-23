# Import the modules
import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVC
import numpy as np
from collections import Counter
import cv2
import os
from sklearn.utils import shuffle

directory = "mid_data/dataset_cleaned"
SizeDir = os.listdir(directory)
images = []
labels = []

ppc=6
cpb=5
tuple_ppc=(6,6)
tuple_cpb=(5,5)
for size in SizeDir:
    catdir = os.listdir(directory+"/"+size)
    for cat in catdir:
        imdir = os.listdir(directory+"/"+size+"/"+cat)
        for im in imdir:
            image = cv2.imread(directory+"/"+size+"/"+cat+"/"+im,0)
            images.append(image)
            if size=='0':
                labels.append("k"+cat)
            else:
                labels.append("b"+cat)
print("data indexed")
images,labels = shuffle(images,labels)
print("data shuffled")
# Extract the hog features
list_hog_fd = []
for feature in images:
    #(y,x) 77 40
    if feature.shape[0] == 34 and feature.shape[1] == 37:
        feature = cv2.resize(feature,(77,40))
    fd = hog(feature, orientations=9, pixels_per_cell=tuple_ppc, cells_per_block=tuple_cpb, visualize=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')
print("hog created")
images = None
list_hog_fd = None
n_estimators = 22
print ("Count of digits in dataset", Counter(labels))
clf = OneVsRestClassifier(BaggingClassifier(SVC(kernel='linear', class_weight='balanced'), max_samples=1.0 / n_estimators, n_estimators=n_estimators))
print("learning")
# Perform the training
clf.fit(hog_features, labels)

# Save the classifier
joblib.dump(clf, "hogbag.pkl", compress=3)

os.system("checkhogbag.py")