import joblib
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.utils import shuffle
import cv2
import os

class Classifier_LSVC:
    def load_data(self):
        directory = "../mid_data/dc"
        SizeDir = os.listdir(directory)
        images = []
        labels = []

        for size in SizeDir:
            catdir = os.listdir(directory+"/"+size)
            for cat in catdir:
                imdir = os.listdir(directory+"/"+size+"/"+cat)
                for im in imdir:
                    image = cv2.imread(directory+"/"+size+"/"+cat+"/"+im,0)
                    images.append(image)
                    labels.append(cat)
        return images,labels

    def shuffle_data(self,images,labels):
        return shuffle(images,labels)

    def find_hog(self,images):   
        hog_features = []
        for image in images:
            hog_feature = hog(image, orientations=9, pixels_per_cell=(4, 4), cells_per_block=(8, 8), visualize=False)
            hog_features.append(hog_feature)
        return np.array(hog_features, 'float64')

    def train_classifier(self,features,labels):
        clf = LinearSVC(class_weight='balanced',max_iter=3000)
        clf.fit(features, labels)
        return clf
    
    def save_classifier(self,clf):
        joblib.dump(clf, "LinearSVC_HOG4_8_CLF.pkl", compress=3)

    def load_classifier(self):
        try:
            self.clf = joblib.load("LinearSVC_HOG4_8_CLF.pkl")
        except:
            self.clf = self.create_classifier()

    def create_classifier(self):
        images, labels = self.load_data()
        images, labels = self.shuffle_data(images,labels)
        features = self.find_hog(images)
        images = None
        clf = self.train_classifier(features,labels)
        features = None
        labels = None
        self.save_classifier(clf)
        return clf
    
    def start_predict(self,directory):
        test_label_list = os.listdir(directory)
        test_images_path = []
        name = []
        for image in test_label_list:
            test_images_path.append(directory+"/"+image)
            name.append(image)
        print("image added")
        test_label_list = None
        image = None
        score = 0
        maxscore = len(test_images_path)
        log = []
        result=[]
        for img_path,real in zip(test_images_path,name):
            image = cv2.imread(img_path,0)
            roi_hog_fd = hog(image, orientations=9, pixels_per_cell=(4,4), cells_per_block=(8,8), visualize=False)
            nbr = self.clf.predict(np.array([roi_hog_fd], 'float64'))
            nb = str(nbr)
            if (nb[2] == real[len(real)-5]):
                score+=1
                log.append("Prediction : "+img_path[12:]+"\n             is_a "+nb+" TRUE")
                result.append("TRUE")
            else:
                log.append("Prediction : "+img_path[12:]+"\n             is_a "+nb+" FALSE")
                result.append("FALSE")
        scoreLog = ("Score : "+str(score)+" of "+str(maxscore)+"\nAccuracy : "+str(100*score/maxscore))
        return log, result, scoreLog, score/maxscore