import os
import time
import subprocess

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call)
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())
	
asd = os.listdir("hasil")

z=[]
if asd:
	lenasd = len(asd)

	asdasd = asd[lenasd-1]
		
	g=[]
	for i in asdasd:
		if i.isalpha() or i == '-' or i== '.':
			pass
		else:
			g.append(i)

	puluhan = 0
	satuan = 0 
	for i in g:
		if i == '_':
			z.append(puluhan*10+satuan)
			puluhan =0
			satuan =0
		else:
			puluhan = satuan
			satuan = int(i)
	z.append(puluhan*10+satuan)
	puluhan =0
	satuan =0
else:
	z.append(1)
	z.append(1)
	z.append(1)
	z.append(1)
	z.append(1)
	
while process_exists('python36.exe'):
	os.system(r'taskkill /IM "python36.exe" /F /T')
	time.sleep(2)
while process_exists('chrome.exe'):
	os.system(r'taskkill /IM "chrome.exe" /F /T')
	time.sleep(2)
while process_exists('chromedriver.exe'):
	os.system(r'taskkill /IM "chromedriver.exe" /F /T')
	time.sleep(2)


time.sleep(1)
os.system(r'initiatehead.bat')
time.sleep(3)
strstr = str(z[0]) + " " + str(z[1])  + " "+ str(z[2])  + " " + str(z[3]) + " " + str(z[4])
proc = subprocess.Popen(["start",'python36', 'newScrape-v2.1-NightBuild.py', str(z[0]), str(z[1]), str(z[2]), str(z[3]), str(z[4])], shell=True)
print(strstr)

def dosomting():
	global proc
	asd = os.listdir("hasil")
	lenasd = len(asd)
	
	asdasd = asd[lenasd-1]
	
	g=[]
	for i in asdasd:
		if i.isalpha() or i == '-' or i== '.':
			pass
		else:
			g.append(i)

	z=[]
	puluhan = 0
	satuan = 0 
	for i in g:
		if i == '_':
			z.append(puluhan*10+satuan)
			puluhan =0
			satuan =0
		else:
			puluhan = satuan
			satuan = int(i)
	z.append(puluhan*10+satuan)
	puluhan =0
	satuan =0
	strstr = str(z[0]) + " "+ str(z[1])  + " "+ str(z[2])  + " " + str(z[3]) + " " + str(z[4])
	while process_exists('python36.exe'):
		os.system(r'taskkill /IM "python36.exe" /F /T')
		time.sleep(2)
	while process_exists('chrome.exe'):
		os.system(r'taskkill /IM "chrome.exe" /F /T')
		time.sleep(2)
	while process_exists('chromedriver.exe'):
		os.system(r'taskkill /IM "chromedriver.exe" /F /T')
		time.sleep(2)
	
	time.sleep(1)
	os.system(r'initiatehead.bat')
	time.sleep(3)
	time.sleep(5)
	proc = subprocess.Popen(["start",'python36', 'newScrape-v2.1-NightBuild.py', str(z[0]),str(z[1]),str(z[2]),str(z[3]), str(z[4])], shell=True)
	time.sleep(3) # <-- There's no time.wait, but time.sleep.
	
	print(strstr)

time.sleep(5)
while True:
	dosomflag = 0
	b = os.listdir("hasil")
	timer = 0
	while timer < 180:
		if not process_exists('python36.exe'):
			dosomting()
			dosomflag = 1
			print("restarted")
			break
		time.sleep(5)
		timer=timer+5
	if b == os.listdir("hasil") and dosomflag == 0:
		dosomting()
		print("restarted")
		time.sleep(10)





