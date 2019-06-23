# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os
import gc
directory = "dataTest32"
test_label_list = os.listdir(directory)
test_images_path = []
name = []
for image in test_label_list:
    test_images_path.append(directory+"/"+image)
    name.append(image[0])
print("image added")
b1=-1
b2=-1
b=-1
asd = [2,4,8]
zxc= [4,8,16]
for i in asd:
    for j in zxc:
        try:
            print("clf loaded")
            # Lad the classifier
            clf = joblib.load("LinearSVC_HOG"+str(i)+"-"+str(j)+"_CLF.pkl")
            score = 0
            maxscore = len(test_label_list)
            for img_path,real in zip(test_images_path,name):
                image = cv2.imread(img_path,0)
                roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(i, i), cells_per_block=(j, j), visualize=False)
                nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
                nb = str(nbr)
                if (nb[2] == real):
                    score+=1
                    #    print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
                #else:
                    #    print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")

            print("I:"+str(i)+"_J:"+str(j)+" - Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))
            if score/maxscore > b:
                b=score/maxscore
                b1=i
                b2=j
            gc.collect()
        except:
            pass
print("best: "+str(b))
print("ppc: "+str(b1))
print("cpb: "+str(b2))