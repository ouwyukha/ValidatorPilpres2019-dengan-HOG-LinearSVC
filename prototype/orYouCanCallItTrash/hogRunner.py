# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np
import os
import gc
        
for i in range(2,10):
    for j in range(2,12-i):
        directory = "dataTest"
        test_label_list = os.listdir(directory)
        test_images_path = []
        name = []
        for image in test_label_list:
                test_images_path.append(directory+"/"+image)
                name.append(image[0])

        # Lad the classifier
        clf = joblib.load("test_ppc"+str(i)+"_cpb"+str(j)+".pkl")
        score = 0
        maxscore = len(test_label_list)
        for img_path,real in zip(test_images_path,name):
                image = cv2.imread(img_path,0)
                roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(i, i), cells_per_block=(j, j), visualize=False)
                nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
                nb = str(nbr)
                if (nb[3] == real):
                    score+=1
                #    print("Prediction : "+img_path+"\tis_a\t"+nb+"\t TRUE")
                #else:
                #    print("Prediction : "+img_path+"\tis_a\t"+nb+"\t FALSE")

        print("I:"+str(i)+"_J:"+str(j)+" - Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(score/maxscore))
        gc.collect()