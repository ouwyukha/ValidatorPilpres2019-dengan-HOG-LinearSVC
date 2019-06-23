# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import os


directory = r"C:\Users\Kyu\Desktop\Validator\ongoing\mid_data\dc"
newdir = r"C:\Users\Kyu\Desktop\Validator\ongoing\mid_data\dataset_CP"
SizeDir = os.listdir(directory)
images = []
labels = []

# Lad the classifier
clf = joblib.load("digits_cls.pkl")
good=0
bad=0
err=0
for size in SizeDir:
    catdir = os.listdir(directory+"//"+size)
    for cat in catdir:
        imdir = os.listdir(directory+"//"+size+"//"+cat)
        for im in imdir:
            image = cv2.imread(directory+"//"+size+"//"+cat+"//"+im)
            ii = image.copy()
            # Convert to grayscale and apply Gaussian filtering
            im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
            # Threshold the image
            ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
            # Find contours in the image
            #ctrs = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            imz, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Get rectangles contains each contour
            rects = [cv2.boundingRect(ctr) for ctr in ctrs]
            # For each rectangular region, calculate HOG features and predict
            # the digit using Linear SVM.
            for rect in rects:
                # Draw the rectangles
                cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 3) 
                # Make the rectangular region around the digit
                leng = int(rect[3] * 1.6)
                pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
                pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
                roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
                # Resize the image
                try:
                    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
                    roi = cv2.dilate(roi, (3, 3))
                    # Calculate the HOG features
                    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualize=False)
                    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
                    nb= str(int(nbr[0]))
                    if nb == cat:
                        print("good "+str(cat))
                        cv2.imwrite(newdir+"//true//"+size+"//"+cat+"//"+im,ii)
                        good+=1
                    else:
                        print("bad "+str(cat))
                        cv2.imwrite(newdir+"//false//"+size+"//"+cat+"//"+im,ii)
                        bad+=1
                except:
                    print("err "+str(cat))
                    cv2.imwrite(newdir+"//error//"+size+"//"+cat+"//"+im,ii)
                    err+=1
print("good: "+str(good))
print("bad: "+str(bad))
print("error: "+str(err))
print("acc : "+str(good/(good+bad+err)))