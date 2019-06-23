# Import the modules
import joblib
from skimage.feature import hog
from joblib import Memory
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter
import cv2
import os

for i in range(5,10):
    for j in range(2,12-i):
            
        directory = "mid_data/dataset_cleaned"
        train_label_list = os.listdir(directory)
        features = []
        labels = []

        for value in train_label_list:
                images = os.listdir(directory+"/"+value)
                for image in images:
                        ig = cv2.imread(directory+"/"+value+"/"+image,0)
                        features.append(ig)
                        labels.append(value)

        # Extract the hog features
        list_hog_fd = []
        for feature in features:
            fd = hog(feature, orientations=9, pixels_per_cell=(i, i), cells_per_block=(j, j), visualize=False)
            list_hog_fd.append(fd)
        hog_features = np.array(list_hog_fd, 'float64')
        print ("Count of digits in dataset", Counter(labels))
        # Create an linear SVM object
        clf = LinearSVC()
        # Perform the training
        clf.fit(hog_features, labels)
        # Save the classifier
        joblib.dump(clf, "test_ppc"+str(i)+"_cpb"+str(j)+".pkl", compress=3)
        mem = Memory("./cachedir",verbose=0)
        mem.clear(warn=False)
os.system('hogRunner.py')