import cv2
import joblib
import numpy as np
import os
import matplotlib.pyplot as plt

directory = "dataTest32"
test_label_list = os.listdir(directory)
test_images_path = []
name = []
for image in test_label_list:
    test_images_path.append(directory+"/"+image)

    name.append(image[0])
print("image added")
sizeDir = None
datdir = None
imdir = None
image = None


clf = joblib.load("pixelonly.pkl")

score = 0
maxscore = len(test_images_path)

for img_path,real in zip(test_images_path,name):
    image = plt.imread(img_path)
    image = image.reshape(32*32*3)
    nbr = clf.predict(np.array([image], 'float64'))
    nb = str(nbr)
    if (nb[3] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")

print("Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))