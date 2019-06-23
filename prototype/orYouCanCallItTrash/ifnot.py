import cv2
import numpy as np
import os

directory = "mid_data/dataset_centered"
directory2 = "mid_data/dataset_splitted_centered"
directory3 = "mid_data/dc"


image=[]
#big and small
#read category
for i, category in enumerate(os.listdir(directory)):
    #read value
    print(category)
    for i, value in enumerate(os.listdir(directory+"/"+category)):
        #read data
        print(value)
        for i, data in enumerate(os.listdir(directory+"/"+category+"/"+value)):
            image.append(data)

for i, category in enumerate(os.listdir(directory2)):
    #read value
    print(category)
    for i, value in enumerate(os.listdir(directory2+"/"+category)):
        #read data
        print(value)
        for i, data in enumerate(os.listdir(directory2+"/"+category+"/"+value)):
            image.append(data)

for i, category in enumerate(os.listdir(directory3)):
    #read value
    print(category)
    for i, value in enumerate(os.listdir(directory3+"/"+category)):
        #read data
        print(value)
        for i, data in enumerate(os.listdir(directory3+"/"+category+"/"+value)):
            if data not in image:
                os.remove(directory3+"/"+category+"/"+value+"/"+data)
                print(directory3+"/"+category+"/"+value+"/"+data+"  has been removed")
            