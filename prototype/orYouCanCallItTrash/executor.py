import cv2
import sklearn
import os
import _pickle as c
import numpy as np
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

def load(clf_file):
    with open(clf_file, 'rb') as file:
        clf = c.load(file)
    return clf

svc = load("trained_svc.mdl")

directory = "dataTest"
test_label_list = os.listdir(directory)

test_images_path = []

surf = cv2.xfeatures2d.SURF_create()

for i, image in enumerate(test_label_list):
        test_images_path.append(directory+"/"+image)
    
##detect feature
descriptor_list = []
for img_path in test_images_path:
        image = cv2.imread(img_path,0)
        h = image.shape[0]
        w = image.shape[1]
        image = cv2.resize(image, (4*w, 4*h), interpolation = cv2.INTER_CUBIC)
        kp, des = surf.detectAndCompute(image,None)
        descriptor_list.append(des)

##stack the features
stacked_descriptor = descriptor_list[0]
for descriptor in descriptor_list[1:]:
    stacked_descriptor = np.vstack((stacked_descriptor,descriptor))

##find feature centroids
centroids, _ = kmeans(stacked_descriptor,100,1)

##prepare features for data test
test_features = np.zeros((len(test_images_path),len(centroids)),"float32")

for i in range(len(test_images_path)):
    words , _ = vq(descriptor_list[i],centroids)
    for w in words:
        test_features[i][w] += 1

##normalizer data -> optional
stdScaler = StandardScaler().fit(test_features)
test_features = stdScaler.transform(test_features)

##prediction
for filename, class_id in zip(test_images_path,svc.predict(test_features)):
    print("Prediction : "+filename+"\tis_a\t"+train_label_list[class_id])