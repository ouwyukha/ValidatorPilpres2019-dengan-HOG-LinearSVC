from __future__ import print_function
import cv2
import numpy as np
import os

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

def alignImages(im1, im2):
	try:
		# Convert images to grayscale
		im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
		im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
		# Detect ORB features and compute descriptors.
		orb = cv2.ORB_create(MAX_FEATURES)
		keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
		keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
		# Match features.
		matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
		matches = matcher.match(descriptors1, descriptors2, None)
		# Sort matches by score
		matches.sort(key=lambda x: x.distance, reverse=False)
		# Remove not so good matches
		numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
		matches = matches[:numGoodMatches]
		# Draw top matches
		imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
		#cv2.imwrite("matches.jpg", imMatches)
		# Extract location of good matches
		points1 = np.zeros((len(matches), 2), dtype=np.float32)
		points2 = np.zeros((len(matches), 2), dtype=np.float32)
		for i, match in enumerate(matches):
			points1[i, :] = keypoints1[match.queryIdx].pt
			points2[i, :] = keypoints2[match.trainIdx].pt
		# Find homography
		h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
		# Use homography
		height, width, channels = im2.shape
		im1Reg = cv2.warpPerspective(im1, h, (width, height))
		return im1Reg, h
	except:
		h="error"
		return im1 , h
 
def translateImage(im1,im2):
	try:
		# Convert images to grayscale
		im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
		im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
		# Detect ORB features and compute descriptors.
		orb = cv2.ORB_create(MAX_FEATURES)
		keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
		keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
		# Match features.
		matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
		matches = matcher.match(descriptors1, descriptors2, None)
		# Sort matches by score
		matches.sort(key=lambda x: x.distance, reverse=False)
		# Remove not so good matches
		numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
		matches = matches[:numGoodMatches]
		# Draw top matches
		imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
		#cv2.imwrite("matches.jpg", imMatches)
		# Extract location of good matches
		points1 = np.zeros((len(matches), 2), dtype=np.float32)
		points2 = np.zeros((len(matches), 2), dtype=np.float32)
		for i, match in enumerate(matches):
			points1[i, :] = keypoints1[match.queryIdx].pt
			points2[i, :] = keypoints2[match.trainIdx].pt
		# Find homography
		h,mask = cv2.estimateAffine2D(points1,points2)
		h[0][0]=1
		h[0][1]=0
		h[1][0]=0
		h[1][1]=1
		#print(h)
		# Use homography
		height, width, channels = im2.shape
		im1Reg = cv2.warpAffine(im1,h,(width,height),borderValue=(255,255,255))
		return im1Reg, h
	except:
		h="error"
		return im1 , h
 

def threshy(im):
	ret,a = cv2.threshold(im,200,255,cv2.THRESH_BINARY)
	return a


if __name__ == '__main__':
	directory = "data/X2"
	for i, filename in enumerate(os.listdir(directory)):
		# Read reference image
		refFilename = "1.jpg"
		refFilename2 = "t2.jpg"
		#print("Reading reference image : ", refFilename)
		#print("Reading reference image : ", refFilename2)
		imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
		imReference2 = cv2.imread(refFilename2, cv2.IMREAD_COLOR)
		
		# Read image to be aligned
		#print("Reading image to align : ", filename);  
		im = cv2.imread(directory+"/"+filename, cv2.IMREAD_COLOR)
		
		#print("Aligning images ...")
		# Registered image will be resotred in imReg. 
		# The estimated homography will be stored in h. 
		imReg, h = alignImages(im, imReference)
		if h == "error" :
			#print("Error occured: ", filename)
			with open("mid_data/aligned/errorLog.txt", 'a+') as f:
				f.write("ErrorImage : "+filename+"\n")
			continue
		imReg, h = translateImage(imReg, imReference)
		if h == "error" :
			#print("Error occured: ", filename)
			with open("mid_data/aligned/errorLog.txt", 'a+') as f:
				f.write("ErrorImage : "+filename+"\n")
			continue

		crop_img = imReg[200:1000, 1020:imReg.shape[1]-40].copy()
		
		crop_img, h = translateImage(crop_img, imReference2)
		
		# Write aligned image to disk. 
		outFilename = "mid_data/aligned/aligned_"+filename
		#print("Saving aligned image : ", outFilename); 
		#cv2.imwrite(outFilename, threshy(crop_img))
		cv2.imwrite(outFilename, crop_img)
		
		# #print estimated homography
		#print("Estimated homography : \n",  h)


