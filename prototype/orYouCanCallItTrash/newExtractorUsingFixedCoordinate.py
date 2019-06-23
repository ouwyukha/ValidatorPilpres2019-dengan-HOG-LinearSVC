import cv2
import os

def threshy(im):
	ret,a = cv2.threshold(im,220,255,cv2.THRESH_BINARY)
	return a

def box_extraction(integre,alignedImageDir,imageName,dataTxtDir,TxtName, targetDir):
	img = cv2.imread(alignedImageDir+"/"+imageName, 0)  # Read the image
	
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
			newTPSData.append("0"+data)
		else:
			newTPSData.append("00"+data)
	htop = 85
	wtop = 48
	hbot = 42
	wbot = 45

	# 1 = top , 0 = bot
	boxes = [
		[5,59,"JOKOWI1",newTPSData[2][0],1],
		[54,59,"JOKOWI2",newTPSData[2][1],1],
		[104,59,"JOKOWI3",newTPSData[2][2],1],
		[5,207,"PRABOWO1",newTPSData[3][0],1],
		[54,207,"PRABOWO2",newTPSData[3][1],1],
		[104,207,"PRABOWO3",newTPSData[3][2],1],
		[5,449,"SAH1",newTPSData[4][0],0],
		[54,449,"SAH2",newTPSData[4][1],0],
		[105,449,"SAH3",newTPSData[4][2],0],
		[5,566,"NOTSAH1",newTPSData[5][0],0],
		[54,566,"NOTSAH2",newTPSData[5][1],0],
		[105,566,"NOTSAH3",newTPSData[5][2],0],
		[5,681,"TOTAL1",newTPSData[6][0],0],
		[54,681,"TOTAL2",newTPSData[6][1],0],
		[105,681,"TOTAL3",newTPSData[6][2],0]
		]

	for box in boxes:
		x, y, title, value, category = box[0],box[1],box[2],box[3],box[4]
		if category:
			h,w = htop,wtop
		else:
			h,w = hbot,wbot
		new_img = img[y+4:y+h-4, x+4:x+w-4]
		new_img = threshy(new_img)
		cv2.imwrite(targetDir +"data_"+imageName[8:len(imageName)-4]+"_"+title+'_'+value+'.jpg', new_img)

alignedImageDir = "mid_data/aligned"
dataTxtDir = "data/text"
targetDir = "valval/"
for i,(imageName,TxtName) in enumerate(zip(os.listdir(alignedImageDir),os.listdir(dataTxtDir))):
	box_extraction(i+1,alignedImageDir,imageName,dataTxtDir,TxtName, targetDir)