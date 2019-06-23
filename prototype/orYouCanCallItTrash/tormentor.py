import cv2
import sklearn
import os
import numpy as np
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

def save(clf,name):
    with open(name, 'wb') as file:
        file.write(clf)

directory = "mid_data/dataset_cleaned"
train_label_list = os.listdir(directory)

train_images_path = []
train_images_label = []

sift = cv2.xfeatures2d.SIFT_create()

for i, value in enumerate(train_label_list):
    images = os.listdir(directory+"/"+value)
    for image in images:
        train_images_path.append(directory+"/"+value+"/"+image)
        train_images_label.append(value)
    
print("image paths has been acquired")
##detect feature
descriptor_list = []
for img_path in train_images_path:
        image = cv2.imread(img_path,0)
        h = image.shape[0]
        w = image.shape[1]
        image2 = cv2.resize(image, (4*w, 4*h), interpolation = cv2.INTER_CUBIC)
        kp, des = sift.detectAndCompute(image2,None)
        descriptor_list.append(des)
        if des is None:
            with open("deslog.txt","a") as f:
                f.write(img_path)
                f.write(" : no descriptor\n")
    
print("descriptors has been generated")
##stack the features
stacked_descriptor = descriptor_list[0]
for descriptor in descriptor_list[1:]:
    stacked_descriptor = np.vstack((stacked_descriptor,descriptor))
    
print("descriptor has been stacked")
##find feature centroids
centroids, _ = kmeans(stacked_descriptor,100,1)
print("centroids has been found")
##prepare features for data train
train_features = np.zeros((len(train_images_path),len(centroids)),"float32")
for i in range(len(train_images_path)):
    words , _ = vq(descriptor_list[i],centroids)
    for w in words:
        train_features[i][w] += 1
print("train features has been created")
##normalizer data -> optional
stdScaler = StandardScaler().fit(train_features)
train_features = stdScaler.transform(train_features)
print("features has been normalized")
##train
svc = LinearSVC()
svc.fit(train_features,np.array(train_images_label))

save(svc, "trained_svc.mdl")
print("train has done")