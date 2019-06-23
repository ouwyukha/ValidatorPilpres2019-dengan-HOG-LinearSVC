import cv2
import numpy as np
import os

def threshy(im):
	ret,a = cv2.threshold(im,125,255,cv2.THRESH_BINARY)
	a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
	return a
	
def clean(im):
	imGray = threshy(im)
	n1 = imGray.copy()
	for x in range(imGray.shape[1]):
		for y in range(imGray.shape[0]):
			n1[y][x]=255
	n2 = n1.copy()
	
	for x in range(imGray.shape[1]):
		score=0
		for y in range(imGray.shape[0]):
			if imGray[y][x] ==0:
				score=score+1
		if score > imGray.shape[0] -1:
			for y in range(imGray.shape[0]):
				n1[y][x]=12
				
	for y in range(imGray.shape[0]):
		score=0
		for x in range(imGray.shape[1]):
			if imGray[y][x] == 0:
				score=score+1
		if score > imGray.shape[1]-1:
			for x in range(imGray.shape[1]):
				n2[y][x]=12
			
	for x in range(imGray.shape[1]):
		for y in range(imGray.shape[0]):
			if n1[y][x]==12:
				imGray[y][x]=255
			if n2[y][x]==12:
				imGray[y][x]=255
				
	return imGray
		
directory = "mid_data/dataset_raw"

#read category
for i, category in enumerate(os.listdir(directory)):
	#read value
	print(category)
	for i, value in enumerate(os.listdir(directory+"/"+category)):
		#read data
		print(value)
		for i, data in enumerate(os.listdir(directory+"/"+category+"/"+value)):
			im = cv2.imread(directory+"/"+category+"/"+value+"/"+data, cv2.IMREAD_COLOR)
			imReg= clean(im)
			outFilename = "mid_data/dataset_cleaned/"+category+"/"+value+"/"+data
			cv2.imwrite(outFilename, imReg)
			#print(outFilename)

