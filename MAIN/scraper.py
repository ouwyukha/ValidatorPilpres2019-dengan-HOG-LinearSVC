from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import requests
import time
import subprocess
import win32con
import win32gui
import wmi

class Scrape_Scraper:
    def open_driver(self):
        subprocess.check_call(['initiatehead.bat'], shell=True, cwd="chromedriver/")

    def check_driver(self):
        winlist = wmi.WMI().Win32_Process()
        for i,proc in enumerate(winlist):
            if proc.Name == 'chrome.exe':
                break
            elif proc.Name != 'chrome.exe' and i == len(winlist)-1:
                self.open_driver()

    def init(self):
        self.check_driver()
        time.sleep(0.2)
        self.dirHasil = "temp/source"
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_driver = "chromedriver/chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
        self.driver.get('https://pemilu2019.kpu.go.id/#/ppwp/hitung-suara/')
        #self.driver.get('https://google.com/')

    def scrape(self):
        locationTemplate = self.driver.find_elements_by_class_name('clear-button')
        if len(locationTemplate) == 5:
            location = []
            time.sleep(0.2)
            for data in locationTemplate:
                location.append(data.get_attribute('innerHTML'))

            provName = location[4]
            kabName = location[3]
            kecName = location[2]
            kelName = location[1]
            tpsName = location[0]

            combineName = provName+"_"+kabName+"_"+kecName+"_"+kelName+"_"+tpsName
            combineName = re.sub(' +', '',combineName)
            combineName = re.sub('\n', '',combineName)
            combineName = re.sub('<!---->', '',combineName)
            combineName = re.sub('<span>-</span>', '',combineName)
            
            print(combineName)
            
            #list tampung suara : 0=dpt - 1=pilih - 2=jokowi - 3=prabowo - 4=sah - 5=tidak sah - 6=total - 7=c1
            m=[]
            # retrieve data
            time.sleep(1)
            while len(m) != 7:
                #cek ketersediaan suara
                alert = self.driver.find_elements_by_class_name('alert')
                if alert:
                    errorLocation = provName+"_"+kabName+"_"+kecName+"_"+kelName+"_"+tpsName
                    print("alert:"+errorLocation)
                    with open("temp/errorLog.txt", 'a+') as f:
                        f.write("DataNotAvail : "+errorLocation+"\n")
                    return -1
                time.sleep(0.2)
                suara = self.driver.find_elements_by_class_name('number')
                m.clear()
                
                for data in suara:
                    m.append(int(data.get_attribute('innerHTML')))

            with open(self.dirHasil+"/text/"+combineName+".txt", 'w') as f:
                f.write(str(m[0])+" "+str(m[1])+" "+str(m[2])+" "+str(m[3])+" "+str(m[4])+" "+str(m[5])+" "+str(m[6]))

            # open document C1
            show = self.driver.find_elements_by_class_name('btn-dark')
            while not show:
                time.sleep(0.2)
                show = self.driver.find_elements_by_class_name('btn-dark')
            self.driver.execute_script("arguments[0].click()", show[0])
            time.sleep(1)
            
            # retrieve c1
            form = self.driver.find_elements_by_class_name('doc-image')
            while not form:
                print("while not form")
                self.driver.execute_script("arguments[0].click()", show[0])
                time.sleep(2)
                form = self.driver.find_elements_by_class_name('doc-image')
                #cek ketersediaan image
                alert = self.driver.find_elements_by_class_name('alert')
                if alert:
                    errorLocation = provName+"_"+kabName+"_"+kecName+"_"+kelName+"_"+tpsName
                    print("alert:"+errorLocation)
                    with open("error/errorLog.txt", 'a') as f:
                        f.write("DataNotAvail : "+errorLocation+"\n")
                    return -1
            
            while len(form) != 2:
                print("while len form !=2")
                form = self.driver.find_elements_by_class_name('doc-image')
                #cek ketersediaan image
                alert = self.driver.find_elements_by_class_name('alert')
                if alert:
                    errorLocation = provName+"_"+kabName+"_"+kecName+"_"+kelName+"_"+tpsName
                    print("alert:"+errorLocation)
                    with open("error/errorLog.txt", 'a') as f:
                        f.write("DataNotAvail : "+errorLocation+"\n")
                    return -1
                time.sleep(1)
            #print("Identified Doc : ",len(form))
            printedDoc = 0
            while printedDoc != 1:
                print("while printedDoc !=1")
                printedDoc = 0
                #print("Saved Doc : ",printedDoc)
                sleeptime =1
                while printedDoc == 0:
                    try:
                        src2 = form[1].get_attribute('src')
                        response = requests.get(src2,verify='chromedriver/c.pem')
                        if response.status_code == 200:
                            print("response 200")
                            with open(self.dirHasil+"/X2/"+combineName+"_X02.jpg", 'wb') as f:
                                f.write(response.content)
                            exists = os.path.isfile(self.dirHasil+"/X2/"+combineName+"_X02.jpg")
                            if exists:
                                printedDoc = 1
                            else:
                                print(response.status_code)
                            time.sleep(sleeptime)
                    except:
                        sleeptime=2
                        time.sleep(sleeptime)	
            return combineName
        return None