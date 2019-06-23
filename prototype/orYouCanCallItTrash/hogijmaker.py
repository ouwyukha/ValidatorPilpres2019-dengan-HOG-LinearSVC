# Import the modules
import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
#from sklearn.linear_model import SGDClassifier
import numpy as np
from collections import Counter
import cv2
import os
from sklearn.utils import shuffle

directory = "mid_data/dataset_centered"
SizeDir = os.listdir(directory)
images = []
labels = []

ppc=8
cpb=8
tuple_ppc=(8,8)
tuple_cpb=(8,8)

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
    fd = hog(feature, orientations=9, pixels_per_cell=tuple_ppc, cells_per_block=tuple_cpb, visualize=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')
print("hog created")
images = None
list_hog_fd = None
print ("Count of digits in dataset", Counter(labels))
# Create an linear SVM object
clf = LinearSVC(class_weight='balanced',max_iter=3000)

print("learning")
# Perform the training
clf.fit(hog_features, labels)

# Save the classifier
joblib.dump(clf, "custom_ppc"+str(ppc)+"_cpb"+str(cpb)+"_new.pkl", compress=3)

os.system("ijcustom.py")