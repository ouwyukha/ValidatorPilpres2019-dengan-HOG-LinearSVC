import cv2
import numpy as np
import os
from math import ceil
WHITE = [255,255,255]

def centerer(gray):
    # threshold to get just the signature (INVERTED)
    retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(thresh_gray,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find object with the biggest bounding box
    mx = (0,0,0,0)      # biggest bounding box so far
    mx_area = 0
    for cont in contours:
        x,y,w,h = cv2.boundingRect(cont)
        area = w*h
        if area > mx_area:
            mx = x,y,w,h
            mx_area = area
    x,y,w,h = mx

    # Output to files
    roi=gray[y:y+h,x:x+w]
    newmultiplier = 0
    if roi.shape[0] > roi.shape[1]:
        newmultiplier = 28/roi.shape[0]
    else:
        newmultiplier = 28/roi.shape[1]
    roi = cv2.resize(roi,(ceil(roi.shape[1]*newmultiplier),ceil(roi.shape[0]*newmultiplier)),cv2.INTER_AREA)
    padded = cv2.copyMakeBorder(roi, 32-roi.shape[0], 32-roi.shape[0], 32-roi.shape[1], 32-roi.shape[1], cv2.BORDER_CONSTANT, value=WHITE)
    padded = cv2.resize(padded,(32,32),cv2.INTER_AREA)
    return padded


directory = "mid_data/dataset_cleaned"

#big and small
#read category
for i, category in enumerate(os.listdir(directory)):
    #read value
    print(category)
    for i, value in enumerate(os.listdir(directory+"/"+category)):
        #read data
        print(value)
        for i, data in enumerate(os.listdir(directory+"/"+category+"/"+value)):
            im = cv2.imread(directory+"/"+category+"/"+value+"/"+data, 0)
            imReg= centerer(im)
            outFilename = "mid_data/dc/"+category+"/"+value+"/"+data
            cv2.imwrite(outFilename, imReg)
            #print(outFilename)

