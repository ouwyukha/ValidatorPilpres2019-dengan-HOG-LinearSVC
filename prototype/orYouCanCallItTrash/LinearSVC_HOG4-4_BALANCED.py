import joblib
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter
import cv2
import os

directory = "mid_data/dc"
SizeDir = os.listdir(directory)
images = []
labels = []

for size in SizeDir:
    catdir = os.listdir(directory+"/"+size)
    for cat in catdir:
        imdir = os.listdir(directory+"/"+size+"/"+cat)
        for im in imdir:
            image = cv2.imread(directory+"/"+size+"/"+cat+"/"+im,0)
            images.append(image)
            labels.append(cat)
sizeDir = None
datdir = None
imdir = None
image = None
print("data indexed")
list_hog_fd = []
for feature in images:
    fd = hog(feature, orientations=9, pixels_per_cell=(4, 4), cells_per_block=(4, 4), visualize=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')
list_hog_fd = None
print ("Count of digits in dataset", Counter(labels))

# Create an linear SVM object
clf = LinearSVC(class_weight='balanced',max_iter=3000)
# Perform the training
print("learning")
clf.fit(hog_features, labels)
hog_features = None

# Save the classifier
joblib.dump(clf, "LinearSVC_HOG4-4_CLF.pkl", compress=3)

os.system("LinearSVC_HOG4-4_BALANCED_predict.py")