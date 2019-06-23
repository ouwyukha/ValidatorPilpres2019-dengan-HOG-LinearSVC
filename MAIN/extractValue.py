import cv2
import numpy as np
import os
from math import ceil 

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15
WHITE = [255,255,255]

def threshy(image):
    _,im_thresh = cv2.threshold(image,200,255,cv2.THRESH_BINARY)
    return im_thresh
    
def alignImages(im1, im2):
    try:
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        
        orb = cv2.ORB_create(MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
        
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)
        
        matches.sort(key=lambda x: x.distance, reverse=False)
        
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]
        
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)
        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt
            
        h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
        
        height, width, _ = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))
        return im1Reg, h
    except:
        h="error"
        return im1 , None
 
def translateImage(im1,im2):
    try:
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        
        orb = cv2.ORB_create(MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
        
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)
        
        matches.sort(key=lambda x: x.distance, reverse=False)
        
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]
        
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)
        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt
      
        h,_ = cv2.estimateAffine2D(points1,points2)
        h[0][0]=1
        h[0][1]=0
        h[1][0]=0
        h[1][1]=1
        
        height, width, _ = im2.shape
        im1Reg = cv2.warpAffine(im1,h,(width,height),borderValue=(255,255,255))
        return im1Reg, h
    except:
        h="error"
        return im1 , None

        
def box_extraction(integre,cropped_image,filename,dataTxtDir,TxtName, targetDir):
    cropped_image = cv2.cvtColor(cropped_image,cv2.COLOR_BGR2GRAY)
    #import TPS Data
    #list tampung suara : 0=dpt - 1=pilih - 2=jokowi - 3=prabowo - 4=sah - 5=tidak sah - 6=total
    TPSData =[]
    newTPSData =[]
    with open(dataTxtDir+"/"+TxtName, 'r') as f:
        data = f.read()
        TPSData = data.split(' ')
    
    for data in TPSData:
        if len(data) == 3:
            newTPSData.append(data)
        elif len(data) == 2:
            newTPSData.append("X"+data)
        else:
            newTPSData.append("XX"+data)
    htop = 85
    wtop = 48
    hbot = 42
    wbot = 45

    # 1 = top , 0 = bot
    boxes = [
        [8,59,"JOKOWI1",newTPSData[2][0],1],
        [57,59,"JOKOWI2",newTPSData[2][1],1],
        [107,59,"JOKOWI3",newTPSData[2][2],1],
        [8,207,"PRABOWO1",newTPSData[3][0],1],
        [57,207,"PRABOWO2",newTPSData[3][1],1],
        [107,207,"PRABOWO3",newTPSData[3][2],1],
        [8,449,"SAH1",newTPSData[4][0],0],
        [57,449,"SAH2",newTPSData[4][1],0],
        [107,449,"SAH3",newTPSData[4][2],0],
        [8,566,"NOTSAH1",newTPSData[5][0],0],
        [57,566,"NOTSAH2",newTPSData[5][1],0],
        [107,566,"NOTSAH3",newTPSData[5][2],0],
        [8,681,"TOTAL1",newTPSData[6][0],0],
        [57,681,"TOTAL2",newTPSData[6][1],0],
        [107,681,"TOTAL3",newTPSData[6][2],0]
        ]
        
    labels=[]
    images=[]

    for box in boxes:
        x, y, code, value, category = box[0],box[1],box[2],box[3],box[4]
        if category:
            h,w = htop,wtop
        else:
            h,w = hbot,wbot
        new_img = cropped_image[y+4:y+h-4, x+4:x+w-4]

        new_img = threshy(new_img)    
        labels.append(targetDir+'/'+TxtName+'_'+code+'_'+str(value)+'.jpg')
        images.append(new_img)

    return labels,images

    
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
            if imGray[y][x] == 0:
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

def centerer(gray):
    retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(thresh_gray,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    mx = (0,0,0,0)
    mx_area = 0
    for cont in contours:
        x,y,w,h = cv2.boundingRect(cont)
        area = w*h
        if area > mx_area:
            mx = x,y,w,h
            mx_area = area
    x,y,w,h = mx
    try:
        roi=gray[y:y+h,x:x+w]
        newmultiplier = 0
        if roi.shape[0] > roi.shape[1]:
            newmultiplier = 28/roi.shape[0]
        elif roi.shape[1] > roi.shape[0]:
            newmultiplier = 28/roi.shape[1]
        roi = cv2.resize(roi,(ceil(roi.shape[1]*newmultiplier),ceil(roi.shape[0]*newmultiplier)),cv2.INTER_AREA)
        padded = cv2.copyMakeBorder(roi, 32-roi.shape[0], 32-roi.shape[0], 32-roi.shape[1], 32-roi.shape[1], cv2.BORDER_CONSTANT, value=WHITE)
        padded = cv2.resize(padded,(32,32),cv2.INTER_AREA)
        return padded
    except:
        return cv2.resize(gray,(32,32),cv2.INTER_AREA)

def crop(directory,filename):
    refFilename = "refImage/refImage1.jpg"
    refFilename2 = "regImage/refImage2.jpg"
    imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
    imReference2 = cv2.imread(refFilename2, cv2.IMREAD_COLOR)
    
    im = cv2.imread(directory+"/"+filename, cv2.IMREAD_COLOR)
    
    imReg, h = alignImages(im, imReference)
    if h is None :
        return im, "error"

    imReg, h = translateImage(imReg, imReference)
    if h is None :
        return im, "error"
    cropped_image = imReg[200:1000, 1020:imReg.shape[1]-40].copy()
    return cropped_image, "not"
        
def main_extract():
    log = 0
    directory = "temp/source/X2"
    dataTxtDir = "temp/source/text"
    targetDir = "temp/result"
    
    isTargetDir = os.listdir(targetDir)
    if isTargetDir:
        for dir in isTargetDir:
            os.remove(targetDir+'/'+dir)
            
    for i,(filename,TxtName) in enumerate(zip(os.listdir(directory),os.listdir(dataTxtDir))):
        cropped_image, h = crop(directory,filename)
        if h == "error":
            print("Error occured: ", filename)
            with open("temp/errorLog.txt", 'a+') as f:
                f.write("ErrorImage : "+filename+"\n")
                continue

        labels,images = box_extraction(i+1,cropped_image,filename,dataTxtDir,TxtName, targetDir)
        for label,image in zip(labels,images):
            better_image = clean(image)
            better_image = centerer(image)
            cv2.imwrite(label, better_image)
            log+=1
    return targetDir, log

if __name__ == "__main__":
    main_extract()
