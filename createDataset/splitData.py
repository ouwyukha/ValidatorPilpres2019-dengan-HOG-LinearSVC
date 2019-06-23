# Import the modules
import os
from sklearn.model_selection import train_test_split
import random

directory = "mid_data/dc"
SizeDir = os.listdir(directory)
newdir = "mid_data/dc_splitted"

def moveFile(dir,file):
	os.rename(directory+"/"+dir+"/"+file, newdir+"/"+dir+"/"+file)

for size in SizeDir:
	catdir = os.listdir(directory+"/"+size)
	for cat in catdir:
		files = os.listdir(directory+"/"+size+"/"+cat)
		iter = 0
		box=[]
		while(iter<100):
			index = random.randrange(0, len(files))
			if index not in box:
				box.append(index)
				iter+=1
				moveFile(size+"/"+cat,files[index])
			
