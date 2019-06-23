import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os
from skimage import data, exposure

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

#clf = joblib.load("LinearSVC_HOG2-16_CLF.pkl")
qwe=4
asd=8
clf = joblib.load("hogBalanced_ppc"+str(qwe)+"_cpb"+str(asd)+".pkl")

score = 0
maxscore = len(test_images_path)

for img_path,real in zip(test_images_path,name):
    image = cv2.imread(img_path,0)
    roi_hog_fd,ii = hog(image, orientations=9, pixels_per_cell=(qwe,qwe), cells_per_block=(asd,asd), visualize=True)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    print(roi_hog_fd.shape)
    #for z in roi_hog_fd:
    #    print(z)
    nb = str(nbr)
    if (nb[3] == real):
        score+=1
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
    else:
        print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")
    
    #ii = exposure.rescale_intensity(ii, in_range=(0, 50))
    #ii=cv2.resize(ii,(250,250))
    cv2.imshow("whatt",ii)
    cv2.waitKey(0)

print("2_16 - Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))