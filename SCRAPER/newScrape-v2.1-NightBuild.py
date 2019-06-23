from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import requests
import time
import argparse

#starting index
pRan=0	#Provinsi
bRan=1	#Kabupaten
cRan=2	#Kecamatan
lRan=3	#Kelurahan
tRan=4	#tps

pError=0
bError=1
cError=2
lError=3
tError=4
misClickFlag = False

# argparse buat passing variable via commandline
parser = argparse.ArgumentParser(description='search')
parser.add_argument('provinsiCode', metavar='pCC', nargs='?', const=1, default=1, type=int)
parser.add_argument('KabupatenCode', metavar='bCC',nargs='?', const=1, default=1, type=int)
parser.add_argument('KecamatanCode', metavar='cCC', nargs='?', const=1, default=1, type=int)
parser.add_argument('KelurahanCode', metavar='lCC', nargs='?', const=1, default=1, type=int)
parser.add_argument('tpsCode', metavar='tCC', nargs='?', const=1, default=1, type=int)
args = parser.parse_args()

print("running")
print(args.provinsiCode,args.KabupatenCode,args.KecamatanCode,args.KelurahanCode,args.tpsCode)

pRan=args.provinsiCode-1	#Provinsi
bRan=args.KabupatenCode		#Kabupaten
cRan=args.KecamatanCode+1	#Kecamatan
lRan=args.KelurahanCode+2	#Kelurahan
tRan=args.tpsCode+3 		#tps

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = r"C:/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

driver.get('https://pemilu2019.kpu.go.id/#/ppwp/hitung-suara/')

def scrape(tpsInt,provName,provInt,kabName,kabInt,kecName,kecInt,kelName,kelInt):
	#location parser start
	tpsTPS = driver.find_elements_by_class_name('clear-button')
	while not tpsTPS:
		time.sleep(1)
		tpsTPS = driver.find_elements_by_class_name('clear-button')
	dirHasil = os.listdir("hasil")
	containerIntBox = []
	containerBox = []
	if dirHasil:
		lenHasil = len(dirHasil)
		topOne = dirHasil[lenHasil-1]
		readyParse=[]
		counter =0
		tempDigit = ""
		for i in topOne:
			if i.isdigit():
				tempDigit = tempDigit + str(i)
				if counter == 1:
					containerIntBox.append(tempDigit)
					counter=0
				else:
					counter = 1
			else:
				readyParse.append(i)
		readyParse = "".join(readyParse)
		readyParse.replace(".txt", "")
		readyParse.replace("_X.png", "")
		temp=""
		for i in readyParse:
			if i == '_':
				containerBox.append(temp)
				temp=""
			else:
				temp=temp+i
	if containerBox and containerIntBox:
		if (int(containerIntBox[0])-1 == provInt and provName != containerBox[0]) or (int(containerIntBox[1]) == kabInt and kabName != containerBox[1]) or (int(containerIntBox[2])+1 == kecInt and kecName != containerBox[2]) or (int(containerIntBox[3])+2 == kelInt and kelName != containerBox[3]):
			print("no match")
			driver.quit()
			exit()
	#location parser end 
	
	global misClickFlag
	aprovInt=str(provInt+1)
	akabInt=str(kabInt)
	akecInt=str(kecInt-1)
	akelInt=str(kelInt-2)
	atpsInt=str(tpsInt-3)
	if provInt+1 < 10:
		aprovInt = "0"+aprovInt
	if kabInt < 10:
		akabInt = "0"+akabInt
	if kecInt-1 < 10:
		akecInt = "0"+akecInt
	if kelInt-2 < 10:
		akelInt = "0"+akelInt
	if tpsInt-3 < 10:
		atpsInt = "0"+atpsInt
	combineName = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt+kelName+"_"+atpsInt
	combineName = re.sub(' +', '',combineName)
	#print("mulai scrape data: ",combineName)
	
	#list tampung suara : 0=dpt - 1=pilih - 2=jokowi - 3=prabowo - 4=sah - 5=tidak sah - 6=total - 7=c1
	m=[]
    # retrieve data
	time.sleep(1)
	while len(m) != 7:
		#cek ketersediaan suara
		alert = driver.find_elements_by_class_name('alert')
		if alert:
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt+kelName+"_"+atpsInt
			print("alert:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
		time.sleep(0.2)
		suara = driver.find_elements_by_class_name('number')
		m.clear()
		try:
			for i, data in enumerate(suara):
				m.append(int(data.get_attribute('innerHTML')))
		except ValueError:
			global pError
			global bError
			global cError
			global lError
			global tError
			pError = provInt
			bError = kabInt
			cError = kecInt
			lError = kelInt
			tError = tpsInt
			misClickFlag = True
			return 0

	with open("hasil/"+combineName+".txt", 'w') as f:
		f.write(str(m[0])+" "+str(m[1])+" "+str(m[2])+" "+str(m[3])+" "+str(m[4])+" "+str(m[5])+" "+str(m[6]))
	# open document C1
	show = driver.find_elements_by_class_name('btn-dark')
	while not show:
		time.sleep(0.2)
		show = driver.find_elements_by_class_name('btn-dark')
	driver.execute_script("arguments[0].click()", show[0])
	time.sleep(1)
	
	#print("mulai scrape image")
    # retrieve c1
	form = driver.find_elements_by_class_name('doc-image')
	while not form:
		print("while not form")
		driver.execute_script("arguments[0].click()", show[0])
		time.sleep(2)
		form = driver.find_elements_by_class_name('doc-image')
		#cek ketersediaan image
		alert = driver.find_elements_by_class_name('alert')
		if alert:
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt+kelName+"_"+atpsInt
			print("alert:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
	
	while len(form) != 2:
		print("while len form !=2")
		form = driver.find_elements_by_class_name('doc-image')
		#cek ketersediaan image
		alert = driver.find_elements_by_class_name('alert')
		if alert:
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt+kelName+"_"+atpsInt
			print("alert:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
		time.sleep(1)
	#print("Identified Doc : ",len(form))
	printedDoc = 0
	while printedDoc != 2:
		print("while printedDoc !=2")
		printedDoc = 0
		#print("Saved Doc : ",printedDoc)
		sleeptime =1
		while printedDoc ==0:
			try:
				src1 = form[0].get_attribute('src')
				response = requests.get(src1,verify='c.pem')
				if response.status_code == 200:
					print("response 200")
					with open("hasil/"+combineName+"_X01.png", 'wb') as f:
						f.write(response.content)
					exists = os.path.isfile("hasil/"+combineName+"_X01.png")
					if exists:
						printedDoc = 1
					else:
						print(response.status_code)
					time.sleep(sleeptime)
			except:
				sleeptime=2
				time.sleep(sleeptime)	
		while printedDoc ==1:
			try:
				src2 = form[1].get_attribute('src')
				response = requests.get(src2,verify='c.pem')
				if response.status_code == 200:
					print("response 200")
					with open("hasil/"+combineName+"_X02.png", 'wb') as f:
						f.write(response.content)
					exists = os.path.isfile("hasil/"+combineName+"_X02.png")
					if exists:
						printedDoc = 2
					else:
						print(response.status_code)
					time.sleep(sleeptime)
			except:
				sleeptime=2
				time.sleep(sleeptime)	
	return 1
	
def funcTPS(tpsInt,provName,provInt,kabName,kabInt,kecName,kecInt,kelName,kelInt):
	global misClickFlag
	global pError
	global bError
	global cError
	global lError
	global tError
	#print(kelName, " - pilih tps")
	tps = driver.find_elements_by_class_name('clear-button')
	while not tps or len(tps) < 5:
		time.sleep(1)
		tps = driver.find_elements_by_class_name('clear-button')
	
	try:
		#cek ketersediaan data
		tpsNameParent = driver.execute_script("return arguments[0].parentNode;", tps[tpsInt])
		tpsNameSlot = driver.execute_script("return arguments[0].parentNode;", tpsNameParent)
	except:
		print("funcTPS quit")
		driver.quit()
		exit()
	try:
		if not tpsNameSlot.find_elements_by_class_name("text-right"):	
			aprovInt=str(provInt+1)
			akabInt=str(kabInt)
			akecInt=str(kecInt-1)
			akelInt=str(kelInt-2)
			atpsInt=str(tpsInt-3)
			if provInt+1 < 10:
				aprovInt = "0"+aprovInt
			if kabInt < 10:
				akabInt = "0"+akabInt
			if kecInt-1 < 10:
				akecInt = "0"+akecInt
			if kelInt-2 < 10:
				akelInt = "0"+akelInt
			if tpsInt-3 < 10:
				atpsInt = "0"+atpsInt
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt+kelName+"_"+atpsInt
			print("nodatafuncTPS:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
	except:
		pass

	time.sleep(1)
	driver.execute_script("arguments[0].click()", tps[tpsInt])
	time.sleep(1)
	guard = scrape(tpsInt,provName,provInt,kabName,kabInt,kecName,kecInt,kelName,kelInt)
	if misClickFlag == True:
		return 0
	return 1

def funcKel(kelInt,provName,provInt,kabName,kabInt,kecName,kecInt):
	global misClickFlag
	global pError
	global bError
	global cError
	global lError
	global tRan
	#print(kecName, " - pilih kelurahan")
	kelurahan = driver.find_elements_by_class_name('clear-button')
	while not kelurahan or len(kelurahan) < 4:
		time.sleep(1)
		kelurahan = driver.find_elements_by_class_name('clear-button')
	try:
		kelName = str(kelurahan[kelInt].get_attribute('innerHTML')).strip()

		#cek ketersediaan data
		kelNameParent = driver.execute_script("return arguments[0].parentNode;", kelurahan[kelInt])
		kelNameSlot = driver.execute_script("return arguments[0].parentNode;", kelNameParent)
	except:
		print("funcKel quit")
		driver.quit()
		exit()
	try:
		if not kelNameSlot.find_elements_by_class_name("text-right"):	
			aprovInt=str(provInt+1)
			akabInt=str(kabInt)
			akecInt=str(kecInt-1)
			akelInt=str(kelInt-2)
			if provInt+1 < 10:
				aprovInt = "0"+aprovInt
			if kabInt < 10:
				akabInt = "0"+akabInt
			if kecInt-1 < 10:
				akecInt = "0"+akecInt
			if kelInt-2 < 10:
				akelInt = "0"+akelInt
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt+kecName+"_"+akelInt
			print("nodatafuncKel:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
	except:
		pass

	time.sleep(1)
	driver.execute_script("arguments[0].click()", kelurahan[kelInt])
	time.sleep(1)
	tpsLEN = len(driver.find_elements_by_class_name('clear-button'))
	while not tpsLEN:
		time.sleep(1)
		tpsLEN = len(driver.find_elements_by_class_name('clear-button'))
	for i in range(tRan,tpsLEN):
		guard = funcTPS(i,provName,provInt,kabName,kabInt,kecName,kecInt,kelName,kelInt)
		if misClickFlag == True:
			return 0
		time.sleep(1)
		if guard == 1 or (guard ==3 and tRan == tpsLEN-1):
			#clearTPS-navigate back
			clearTPS = driver.find_elements_by_class_name('clear')
			time.sleep(1)
			driver.execute_script("arguments[0].click()", clearTPS[6])
			print("trigger tpsclear")
			time.sleep(1)
	tRan =4
	return 1
    
def funcKec(kecInt,provName,provInt,kabName,kabInt):
	global misClickFlag
	global pError
	global bError
	global cError
	global lRan
	#print(kabName," - pilih kecamatan")
	kecamatan = driver.find_elements_by_class_name('clear-button')
	while not kecamatan or len(kecamatan) < 3:
		time.sleep(1)
		kecamatan = driver.find_elements_by_class_name('clear-button')
	try:
		kecName = str(kecamatan[kecInt].get_attribute('innerHTML')).strip()
	
		#cek ketersediaan data
		kecNameParent = driver.execute_script("return arguments[0].parentNode;", kecamatan[kecInt])
		kecNameSlot = driver.execute_script("return arguments[0].parentNode;", kecNameParent)
	except:
		print("funcKec quit")
		driver.quit()
		exit()
	try:
		if not kecNameSlot.find_elements_by_class_name("text-right"):			
			aprovInt=str(provInt+1)
			akabInt=str(kabInt)
			akecInt=str(kecInt-1)
			if provInt+1 < 10:
				aprovInt = "0"+aprovInt
			if kabInt < 10:
				akabInt = "0"+akabInt
			if kecInt-1 < 10:
				akecInt = "0"+akecInt
			errorLocation = aprovInt+provName+"_"+akabInt+kabName+"_"+akecInt
			print("nodatafuncKec:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
	except:
		pass

	time.sleep(1)
	driver.execute_script("arguments[0].click()", kecamatan[kecInt])
	time.sleep(1)	
	kelurahanLEN = len(driver.find_elements_by_class_name('clear-button'))
	while not kelurahanLEN:
		time.sleep(1)
		kelurahanLEN = len(driver.find_elements_by_class_name('clear-button'))
	for i in range(lRan,kelurahanLEN):
		guard = funcKel(i,provName,provInt,kabName,kabInt,kecName,kecInt)
		if misClickFlag == True:
			return 0
		if guard == 1 or (guard == 3 and lRan == kelurahanLEN-1):
			#clearKel-navigate back
			clearKel = driver.find_elements_by_class_name('clear')
			time.sleep(1)
			driver.execute_script("arguments[0].click()", clearKel[5])
			print("trigger kelclear")
			time.sleep(1)
	lRan=3
	return 1

def funcKab(kabInt,provName,provInt):
	global misClickFlag
	global pError
	global bError
	global cRan
	#print(provName," - pilih kabupaten")
	kabupaten = driver.find_elements_by_class_name('clear-button')
	while not kabupaten or len(kabupaten) < 2:
		time.sleep(1)
		kabupaten = driver.find_elements_by_class_name('clear-button')
	try:
		kabName = str(kabupaten[kabInt].get_attribute('innerHTML')).strip()
	
		#cek ketersediaan data
		kabNameParent = driver.execute_script("return arguments[0].parentNode;", kabupaten[kabInt])
		kabNameSlot = driver.execute_script("return arguments[0].parentNode;", kabNameParent)	
	except:
		print("funcKab quit")
		driver.quit()
		exit()
	try:
		if not kabNameSlot.find_elements_by_class_name("text-right"):
			aprovInt=str(provInt+1)
			akabInt=str(kabInt)
			if provInt+1 < 10:
				aprovInt = "0"+aprovInt
			if kabInt < 10:
				akabInt = "0"+akabInt
			errorLocation = aprovInt+provName+"_"+akabInt
			print("nodatafuncKab:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : "+errorLocation+"\n")
			return 3
	except:
		pass

	time.sleep(1)
	driver.execute_script("arguments[0].click()", kabupaten[kabInt])
	time.sleep(1)
	kecamatanLEN = len(driver.find_elements_by_class_name('clear-button'))
	while not kecamatanLEN:
		time.sleep(1)
		kecamatanLEN = len(driver.find_elements_by_class_name('clear-button'))

	for i in range(cRan,kecamatanLEN):
		guard = funcKec(i,provName,provInt,kabName,kabInt)
		if misClickFlag == True:
			return 0
		if guard == 1 or (guard == 3 and i == kecamatanLEN-1):
			#clearKec-navigate back
			clearKec = driver.find_elements_by_class_name('clear')
			time.sleep(1)
			driver.execute_script("arguments[0].click()", clearKec[4])
			print("trigger kecclear")
			time.sleep(1)
	cRan=2
	return 1

def funcProv(provInt):
	global bRan
	global misClickFlag
	#print("pilih provinsi")
	provinsi = driver.find_elements_by_class_name('clear-button')
	while not provinsi or len(provinsi) < 35:
		time.sleep(1)
		provinsi = driver.find_elements_by_class_name('clear-button')
	try:
		provName = str(provinsi[provInt].get_attribute('innerHTML')).strip()
		
		#cek ketersediaan data
		provNameParent = driver.execute_script("return arguments[0].parentNode;", provinsi[provInt])
		provNameSlot = driver.execute_script("return arguments[0].parentNode;", provNameParent)
	except:
		print("funcProv quit")
		driver.quit()
		exit()
	try:
		if not provNameSlot.find_elements_by_class_name("text-right"):
			aprovInt=str(provInt+1)
			if provInt+1 < 10:
				aprovInt = "0"+aprovInt
			errorLocation = aprovInt
			print("nodatafuncProv:"+errorLocation)
			with open("error/errorLog.txt", 'a') as f:
				f.write("DataNotAvail : Provinsi No."+errorLocation+"\n")
			return 3
	except:
		pass

	time.sleep(1)
	driver.execute_script("arguments[0].click()", provinsi[provInt])
	time.sleep(1)
	kabupatenLEN = len(driver.find_elements_by_class_name('clear-button'))
	while not kabupatenLEN:
		time.sleep(1)
		kabupatenLEN = len(driver.find_elements_by_class_name('clear-button'))
	for i in range(bRan,kabupatenLEN):
		guard = funcKab(i,provName,provInt)
		if misClickFlag == True:
			return 0
		if guard == 1 or (guard == 3 and i == kabupatenLEN-1):
			#clearKab-navigate back
			clearKab = driver.find_elements_by_class_name('clear')
			time.sleep(1)
			driver.execute_script("arguments[0].click()", clearKab[3])
			print("trigger kabclear")
			time.sleep(1)
	bRan=1
	return 1

#print("Scraping...")
provinsiLEN = 0
while provinsiLEN != 35:
	provinsiLEN = len(driver.find_elements_by_class_name('clear-button'))

finished = False
while finished == False:
	for i in range(pRan,provinsiLEN):
		funcProv(i)
		#clearProv-navigate back
		clearProv = driver.find_elements_by_class_name('clear')
		time.sleep(1)
		driver.execute_script("arguments[0].click()", clearProv[2])
		print("trigger provclear")
		time.sleep(1)
		#misClick handling
		if misClickFlag == True:
			pRan=pError
			bRan=bError
			cRan=cError
			lRan=lError			
			tRan=tError
			time.sleep(1)
			break
	if misClickFlag == False:
		finished = True
driver.quit()