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

directory = "mid_data/dataset_cleaned"
SizeDir = os.listdir(directory)
images = []
labels = []

ppc=7
cpb=7
tuple_ppc=(7,7)
tuple_cpb=(7,7)
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
# Extract the hog features
list_hog_fd = []
for feature in images:
    #(y,x) 98 49
    feature = cv2.resize(feature,(98,49))
    fd = hog(feature, orientations=9, pixels_per_cell=tuple_ppc, cells_per_block=tuple_cpb, visualize=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')
print("hog created")
images = None
list_hog_fd = None
print ("Count of digits in dataset", Counter(labels))

# Create an linear SVM object
clf = LinearSVC(class_weight='balanced',max_iter=3000)

#clf = SGDClassifier(loss='log',alpha=0.0001,max_iter=2000,tol=1e-4,n_jobs=-1,)
print("learning")
# Perform the training
clf.fit(hog_features, labels)

# Save the classifier
joblib.dump(clf, "crafted_ppc"+str(ppc)+"_cpb"+str(cpb)+"_new.pkl", compress=3)

os.system("ijcrafted.py")