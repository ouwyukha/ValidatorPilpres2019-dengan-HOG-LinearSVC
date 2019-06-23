import os
dirtxt = "data/text"
diralign = "mid_data/aligned"
log = open('log.txt','w')
for i, (fileImg, fileTxt) in enumerate(zip(os.listdir(diralign),os.listdir(dirtxt))):
	#TPS Location : Provinsi - Kabupaten - Kecamatan - Kelurahan - TPS No
	fileTxtWOE = fileTxt[:len(fileTxt)-4]
	localLocation = fileTxtWOE.split('_')
	#print(localLocation)

	#import TPS Data
	#list tampung suara : 0=dpt - 1=pilih - 2=jokowi - 3=prabowo - 4=sah - 5=tidak sah - 6=total
	TPSData =[]
	with open(dirtxt+"/"+fileTxt, 'r') as f:
		data = f.read()
		TPSData = list(map(int, data.split(' ')))
		for number in TPSData:
			print(number)
	
	# Validator_Phase#01 : In-Web MISMATCH
	for data in TPSData[1:]:
		if TPSData[0] < data:
			log.write("TPSData ERROR_CODE:01 - DPT is LESSER\n")
			log.write(fileTxtWOE)
			log.write("\n")
			break
	if TPSData[1] != TPSData[6]:
		log.write("TPSData ERROR_CODE:02 - Pilih + Total not MATCH\n")
		log.write(fileTxtWOE)
		log.write("\n")
	if TPSData[2]+TPSData[3] != TPSData[4]:
		log.write("TPSData ERROR_CODE:03 - Jokowi + Prabowo not MATCH\n")
		log.write(fileTxtWOE)
		log.write("\n")
	if TPSData[4]+TPSData[5] != TPSData[6]:
		log.write("TPSData ERROR_CODE:04 - Sah + Tidak Sah not MATCH\n")
		log.write(fileTxtWOE)
		log.write("\n")
