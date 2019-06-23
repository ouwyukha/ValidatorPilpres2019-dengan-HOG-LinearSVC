
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import io
import base64
from LinearSVC_HOG4_8_BALANCED import Classifier_LSVC
from extractValue import main_extract
from scraper import Scrape_Scraper
import win32gui
import win32con
import keyboard
import re
import cv2
import psutil

def enum_callback(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

dirHasil = "temp/result"
dirSource = "temp/source"

sampah = os.listdir(dirSource+'/X2')
if sampah:
    for trash in sampah:
        os.remove(dirSource+'/X2/'+trash)
sampah = os.listdir(dirSource+'/text')
if sampah:
    for trash in sampah:
        os.remove(dirSource+'/text/'+trash)

clf_factory = Classifier_LSVC()
clf_factory.load_classifier()
scrapy = Scrape_Scraper()
scrapy.init()

toplist = []
winlist = []
win32gui.EnumWindows(enum_callback, toplist)
chrome = [(hwnd, title) for hwnd, title in winlist if 'google chrome' in title.lower()]
chrome = chrome[0]

def myExitHandler():
    win32gui.PostMessage(chrome[0], win32con.WM_CLOSE, 0, 0)
    for proc in psutil.process_iter():
        if "chromedriver" in proc.name():
            proc.kill()
            
def iconFromBase64(base64):
    #extract icon from b64string _C:icon
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

class X2Popup(QtWidgets.QScrollArea):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
    
    def createContent(self,X2file):
        self.X2file = re.sub(r"\.txt.+", '',X2file[:len(X2file)-4])
        self.X2file = self.X2file + '_X02.jpg'
        imageContainer = QtWidgets.QLabel()
        self.image = QtGui.QPixmap(dirSource+'/X2/'+self.X2file)
        if self.image.width() != 0:
            imageContainer.setPixmap(self.image)
            imageContainer.setGeometry(0,0,self.image.width(),self.image.height())
            self.resize(self.image.width(),738)
        else:
            screen = QtWidgets.QDesktopWidget().screenGeometry()
            imageContainer.setGeometry(0,0,600,200)
            imageContainer.setAlignment(QtCore.Qt.AlignCenter)
            imageContainer.setText("No Image Found! Have you deleted it?")
            imageContainer.setStyleSheet("QLabel {color : #FFFFFF;background-color:rgb(30,30,30)}")
            imageContainer.setFont(QtGui.QFont("Sunflower", 20, QtGui.QFont.Normal))
            self.setGeometry((screen.width()/2)-300,(screen.height()/2)-100,imageContainer.width(),imageContainer.height())
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setEnabled(False)
        self.setWidget(imageContainer)
        self.setWindowTitle(self.X2file)
        self.setWindowIcon(iconFromBase64(ico))
        self.setFixedSize(self.size())

class imagePop(QtWidgets.QWidget):
    def __init__(self): 
        QtWidgets.QWidget.__init__(self)

    def createContent(self,selectedText,selected):
        self.yes_false= ""
        self.selectedText = selectedText
        self.text = re.sub(r"\n", '',selectedText)
        self.text = re.sub(r" ", '',self.text)
        self.text = re.sub(r"'\]FALSE", ' FALSE',self.text)
        self.text = re.sub(r"'\]TRUE", ' TRUE',self.text)
        self.text = re.sub(r"is_a\['", ' ',self.text)
        self.text = self.text.split()
        #window
        self.setWindowTitle(self.text[0])
        self.setStyleSheet("QWidget {background-color : rgb(30,30,30)}")
        self.setWindowIcon(iconFromBase64(ico))
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        #button
        self.buttonFont = QtGui.QFont("PrimeTime", 15, QtGui.QFont.Normal) 
        self.yesBtn = QtWidgets.QPushButton(self)
        self.yesBtn.setGeometry(QtCore.QRect(10,355,190,40))
        self.yesBtn.setStyleSheet("QPushButton {background-color : rgb(104,33,122);color : #FFFFFF;} QPushButton::hover{background-color : rgb(30,30,30);color : #FFFFFF;}")
        self.yesBtn.setText("YES")
        self.yesBtn.setFont(self.buttonFont)
        self.noBtn = QtWidgets.QPushButton(self)
        self.noBtn.setGeometry(QtCore.QRect(210,355,190,40))
        self.noBtn.setStyleSheet("QPushButton {background-color : rgb(104,33,122);color : #FFFFFF;} QPushButton::hover{background-color : rgb(30,30,30);color : #FFFFFF;}")
        self.noBtn.setText("NO")
        self.noBtn.setFont(self.buttonFont)
        #image
        self.imageContainer = QtWidgets.QLabel(self)
        self.image = QtGui.QPixmap(dirHasil+'/'+self.text[0])
        self.image = self.image.scaledToWidth(320)
        self.imageContainer.setPixmap(self.image)
        self.imageContainer.setGeometry(45,0,320,320)
        #self.text
        self.textQuestion = QtWidgets.QLabel(self)
        self.textQuestion.setGeometry(0,325,410,20)
        self.textQuestion.setAlignment(QtCore.Qt.AlignCenter)
        self.textQuestion.setText("Is the image above " + str(self.text[0][len(self.text[0])-5]) + " ?")
        self.textQuestion.setStyleSheet("QLabel {color : #FFFFFF;background-color:None}")
        self.textQuestion.setFont(QtGui.QFont("Sunflower", 12, QtGui.QFont.Normal))
    
        self.noBtn.clicked.connect(self.no_func)

    def yes_func(self,selectedText):
        if(self.text[2] == 'FALSE'):
            self.yes_false = "Prediction : " + selectedText[:len(selectedText)-9] + self.text[0][len(self.text[0])-5] + "'] TRUE"
    
    def no_func(self):
        #if(self.text[2] == 'TRUE'):
        self.X2 = X2Popup()
        self.X2.setGeometry(QtCore.QRect(30, 30, 100, 100))
        self.X2.createContent(self.text[0])
        self.X2.show()
        self.close()
            
class Ui_main(object):
    def setupUi(self, main):
        #definite war
        main.setObjectName("main")
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        main.setGeometry(0, 0, self.screen.width(), self.screen.height())  
        main.showMaximized()
        main.setWindowIcon(iconFromBase64(ico))
        main.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        main.setStyleSheet("QWidget {background-color : #000000}")
        self.buttonFont = QtGui.QFont("PrimeTime", 30, QtGui.QFont.Normal) 
        self.browseBtn = QtWidgets.QPushButton(main)
        self.browseBtn.setGeometry(QtCore.QRect(34, 500, 410, 180))
        self.browseBtn.setObjectName("browseBtn")
        self.browseBtn.setFont(self.buttonFont)
        self.browseBtn.setStyleSheet("QPushButton {background-color : rgb(104,33,122);color : #FFFFFF;}QPushButton::hover{background-color : rgb(30,30,30);color : #FFFFFF;}")
        self.clearBtn = QtWidgets.QPushButton(main)
        self.clearBtn.setGeometry(QtCore.QRect(478, 500, 410, 180))
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFont(self.buttonFont)
        self.clearBtn.setStyleSheet("QPushButton {background-color : rgb(104,33,122);color : #FFFFFF;}QPushButton::hover{background-color : rgb(30,30,30);color : #FFFFFF;}")
        self.compareBtn = QtWidgets.QPushButton(main)
        self.compareBtn.setGeometry(QtCore.QRect(922, 500, 410, 180))
        self.compareBtn.setObjectName("compareBtn")
        self.compareBtn.setFont(self.buttonFont)
        self.compareBtn.setStyleSheet("QPushButton {background-color : rgb(104,33,122);color : #FFFFFF;}QPushButton::hover{background-color : rgb(30,30,30);color : #FFFFFF;}")
        self.itemList = QtWidgets.QListWidget(main)
        self.itemList.setGeometry(QtCore.QRect(34, 34, 410, 432))
        self.itemList.setObjectName("itemList")
        self.itemList.setStyleSheet("QListWidget {background-color : rgb(30,30,30);color : #FFFFFF;border:0px}")
        self.textLog = QtWidgets.QListWidget(main)
        self.textLog.setGeometry(QtCore.QRect(478, 34, 854, 432))
        self.textLog.setObjectName("self.textLog")
        self.textLog.setSelectionMode(1)
        self.textLog.setStyleSheet("QListWidget {background-color : rgb(30,30,30);color : #FFFFFF;border:0px}")
        self.browseSubLabel = QtWidgets.QLabel(main)
        self.browseSubLabel.setGeometry(QtCore.QRect(80, 645, 364, 30))
        self.browseSubLabel.setObjectName("browseSubLabel")
        self.subLabelButtonFont = QtGui.QFont("PrimeTime", 10, QtGui.QFont.Normal) 
        self.browseSubLabel.setFont(self.subLabelButtonFont)
        self.browseSubLabel.setStyleSheet("QLabel {color : #FFFFFF;background-color:None}")
        self.maxScore = QtWidgets.QMessageBox()
        self.maxScore.setGeometry(QtCore.QRect((self.screen.width()/2)-100,(self.screen.height()/2)-75,1,1))
        self.maxScore.setWindowTitle("Wrong Data Not Found!")
        self.maxScore.setStyleSheet("QMessageBox{background-color:rgb(30,30,30)}QLabel {color : #FFFFFF;background-color:rgb(30,30,30)}")
        #window translater
        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

        #button trigger
        self.browseBtn.clicked.connect(self.browse_func)
        self.clearBtn.clicked.connect(self.clearList)
        self.compareBtn.clicked.connect(self.predict_func)
        self.textLog.itemClicked.connect(self.show_info_func)

    def retranslateUi(self, main):
        #retranslate window / refresher
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Validator Situng Pilpres 2019"))
        self.browseBtn.setText(_translate("main", "BROWSE"))
        self.browseSubLabel.setText(_translate("browseBtn", "( WHEN READY, PRESS SHIFT ON TPS PAGE )"))
        self.clearBtn.setText(_translate("main", "CLEAR"))
        self.compareBtn.setText(_translate("main", "COMPARE"))

    def browse_func(self):
        win32gui.SetForegroundWindow(chrome[0])
        win32gui.ShowWindow(chrome[0], win32con.SW_MAXIMIZE)
        keyboard.wait('shift')
        log = scrapy.scrape()
        if log:
            self.textLog.addItem(log+' has been added')
            self.itemList.addItem(log)
        else:
            self.textLog.addItem(chrome[1]+' is the wrong page, please check again. If the problem still persists, contact your administrator')
        self.textLog.scrollToBottom()
        self.itemList.scrollToBottom()
        win32gui.ShowWindow(chrome[0], win32con.SW_MINIMIZE)

    def clearList(self):
        isdel = False
        isX2 = os.listdir(dirSource+'/X2')
        if isX2:
            for X2dir in isX2:
                os.remove(dirSource+'/X2/'+X2dir)
                self.textLog.addItem('X2/'+X2dir+' has been removed')
            isdel = True
        isText = os.listdir(dirSource+'/text')
        if isText:
            for self.textdir in isText:
                os.remove(dirSource+'/text/'+self.textdir)
                self.textLog.addItem('text/'+self.textdir+' has been removed')
            isdel = True
        self.itemList.clear()
        if isdel == False:
            self.textLog.addItem('No document to be removed')
        self.textLog.scrollToBottom()


    def predict_func(self):
        self.targetDir,extractLog = main_extract()
        if extractLog:
            self.textLog.addItem(str(extractLog) +" values has been extracted")
            self.textLog.addItem("Starting to predict..")
            self.textLog.scrollToBottom()
            predictLog, resultLog, scoreLog, score = clf_factory.start_predict(self.targetDir)
            for data,resLog in zip(predictLog,resultLog):
                if resLog == "FALSE":
                    newItem = QtWidgets.QListWidgetItem(data)
                    newItem.setBackground(QtGui.QColor("#c8b4ff"))
                    self.textLog.addItem(newItem)                
                else:
                    self.textLog.addItem(data)
            #self.textLog.addItem(scoreLog)
            self.textLog.addItem("Predict has been finished")
            if score == 1:
                self.maxScore.setText(str(extractLog)+"/"+str(extractLog)+" data are valid")
                self.maxScore.exec_()
            self.textLog.scrollToBottom()
        else:
            self.textLog.addItem("No values has been extracted, please browse the document first")
            self.textLog.scrollToBottom()

    def show_info_func(self):
        selected = self.textLog.selectedItems()[0]
        selectedText = selected.text()
        if selectedText[:10] == "Prediction":
            self.imagePopup = imagePop()
            self.imagePopup.setGeometry(QtCore.QRect(34, 88, 410, 401))
            self.imagePopup.createContent(selectedText[13:],selected)
            self.imagePopup.hide()
            self.imagePopup.show()
            self.imagePopup.yesBtn.clicked.connect(self.check_yes_false)
        else:
            try:
                self.imagePopup.close()
            except:
                pass
                
    def check_yes_false(self):
        self.imagePopup.yes_func(self.imagePopup.selectedText)
        if self.imagePopup.yes_false:
            self.textLog.selectedItems()[0].setText(self.imagePopup.yes_false)
            self.textLog.selectedItems()[0].setBackground(QtGui.QColor("transparent"))
        self.imagePopup.close()

#b64 string of purple egg icon (probably 128p x 128p) _C:icon
ico=b"iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAM9SURBVHhe7d2xbSVVGIZhQxekVLEpIT0sNVALARVAD4Sk28ImpETUAFgaCcn6ZQ2au/POnPs8kuWJrVdH99MZ2199+Panv18g8vX2HRICJCVAUgIkJUBSAiQlQFICJCVAUk93E/Lpjx+3p96/P/vt6Xk5AUkJkJQASQmQ1NIjZBocn37/c3t6jA/ffbM9/eeX73/dnt73w28ft6f3rTxWnICkBEhKgKQESGqZEbL3huNKI2QyDRMjBL4QAZISICkBkrrlCDnjhmOvR4+Qyco3Jk5AUgIkJUBSAiR1qRFS3WYcMY2QyaOHyeSOtyhOQFICJCVAUgIkdfkRMn14nz5sP9swWeV2xAlISoCkBEhKgKSyEbJ3cEz2fgC/4zB5NCME3iFAUgIkJUBStxwhk6vfjlSm8XOlYeIEJCVAUgIkJUBSAiQlQFICJCVAUgIkdcpNyBm3HhM3IbMr3Y44AUkJkJQASQmQ1OVHiMHxeEYIbARISoCkBEgqGyFHGByzI7/8boTwlARISoCkBEjq4SNkGhxGw+PtHRxHbpzOGCZOQFICJCVAUgIkJcCFvA6Ot19XJ0BSAiQlQFICJCVAUgIkJUBSAiQlQFKHXsfy6lVneh3r0TcfP3/+a3v6cpyApARISoCkBEhq6REyfVBfZSSdMULO+D0RJyApAZISICkBklpmhBz5y1B7XX1gTY4MEyOE5QmQlABJCZDULUfIkcGx90P5Hf8/yRlDzAhhKQIkJUBSAiS1zAg54y9BPds/Tpx+zkYISxEgKQGSEiApAf4Pr0Pn7RfHCJCUAEkJkJQASS0T4Ostxdsvrs8JSEqApARISoCkDr2ONVn5Fa29w+aOr2Od8erVxAlISoCkBEhKgKSWHiF7TWPF4DiHE5CUAEkJkJQAST18hExW+VO+dxwcEyMENgIkJUBSAiR1ygiZTMNkssoH/8mRQXRENTgmTkBSAiQlQFICJJWNkL2udItyxN7Bsff3WPa+LnalwTFxApISICkBkhIgqcuPkMkdb1GmEXJkcFx9XOzlBCQlQFICJCVAUrccIXvtHStXt8rgmDgBSQmQlABJCZDU0iOE63MCkhIgKQGSEiChl5d/AG2mJMp4S80KAAAAAElFTkSuQmCC"

#int main(){}
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler)
    main = QtWidgets.QDialog()
    ui = Ui_main()
    ui.setupUi(main)
    main.show()
    sys.exit(app.exec_())