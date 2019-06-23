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

for size in SizeDir:
    catdir = os.listdir(directory+"/"+size)
    for cat in catdir:
        imdir = os.listdir(directory+"/"+size+"/"+cat)
        for im in imdir:
            image = cv2.imread(directory+"/"+size+"/"+cat+"/"+im,0)
            if image.shape[0] == 34 and image.shape[1] == 37:
                image = cv2.resize(image,(77,40))
            images.append(image)
            if size=='0':
                    labels.append("k"+cat)
            else:
                    labels.append("b"+cat)

print("data indexed")
image = np.array(image, 'float64')
print ("Count of digits in dataset", Counter(labels))

# Create an linear SVM object
clf = LinearSVC(class_weight='balanced',verbose=1,max_iter=3000)

#clf = SGDClassifier(loss='log',alpha=0.0001,max_iter=2000,tol=1e-4,n_jobs=-1,)
print("learning")
# Perform the training
clf.fit(hog_features, labels)

# Save the classifier
joblib.dump(clf, "beta_test_ppc4_cpb5_new.pkl", compress=3)

os.system("i4j5new.py")