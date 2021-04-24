# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
import time
from ast import literal_eval
from threading import Thread
from datetime import datetime
import pyautogui
#from pywinauto.keyboard import send_keys

# creating main window class
class MainWindow(QMainWindow):
    toHtmlFinished = pyqtSignal()
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.bMain = True
        self.bReloadFirst = False
        self.bLoginFirst = False
        self.bLogin = False
        self.bGo2GChange = False
        self.b2GChange = False
        self.bGo5GChange = False
        self.b5GChange = False
        self.bSecurityChange = False
        self.bChannelChange = False
        self.bHasChanged = False
        self.bSaveSetting = False
        self.brequestF5 = False
        self.bEnter = False
        self.bSearch = False
        self.bGet = False
        #---------------------------
        self.bLogin = True
        self.bAllowTest = True
        self.bClose = False
        #---------------------------
        self.linkconfig = 'http://10.0.0.1/wireless_network_configuration.php'
        self.link2GHz = 'http://10.0.0.1/wireless_network_configuration_edit.php?id=1'
        self.link5GHz = 'http://10.0.0.1/wireless_network_configuration_edit.php?id=2'
        # creating a QWebEngineView
        self.browser = QWebEngineView()
        self.resize(1080, 768)

        # setting default browser url as google
        self.browser.setUrl(QUrl("http://10.0.0.1/"))

        self.browser.loadStarted.connect(self.loadStartedHandler)
        self.browser.loadProgress.connect(self.loadProgressHandler)
        self.browser.loadFinished.connect(self.loadFinishedHandler)
        # adding action when url get changed
        self.browser.urlChanged.connect(self.update_urlbar)
        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)
        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)
        # creating a status bar object
        self.status = QStatusBar()
        # adding status bar to the main window
        self.setStatusBar(self.status)
        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")
        # adding this tool bar tot he main window
        self.addToolBar(navtb)
        # adding actions to the tool bar
        # creating a action for back
        back_btn = QAction("Back", self)
        # setting status tip
        back_btn.setStatusTip("Back to previous page")
        # adding action to the back button
        # making browser go back
        back_btn.triggered.connect(self.browser.back)
        # adding this action to tool bar
        navtb.addAction(back_btn)
        # similarly for forward action
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        # adding action to the next button
        # making browser go forward
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)
        # similarly for reload action
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)
        # similarly for home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # similarly for login action
        login_btn = QAction("Login", self)
        login_btn.setStatusTip("Login")
        login_btn.triggered.connect(self.navigate_login)
        navtb.addAction(login_btn)
        # similarly for start action
        pending_btn = QAction("PR Pending", self)
        pending_btn.setStatusTip("PR Pending")
        pending_btn.triggered.connect(self.SaveSetting)
        navtb.addAction(pending_btn)
        # similarly for start action
        finish_btn = QAction("PR Finnish", self)
        finish_btn.setStatusTip("PR Finnish")
        finish_btn.triggered.connect(self.SaveSetting)
        navtb.addAction(finish_btn)
        # similarly for get action
        get_btn = QAction("Get", self)
        get_btn.setStatusTip("Get")
        get_btn.triggered.connect(self.navigate_get)
        navtb.addAction(get_btn)
        # adding a separator in the tool bar
        navtb.addSeparator()
        # creating a line edit for the url
        self.urlbar = QLineEdit()
        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # adding this to the tool bar
        navtb.addWidget(self.urlbar)
        # adding stop action to the tool bar
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        # adding action to the stop button
        # making browser to stop
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)
        # showing all the components
        self.show()
        # method for updating the title of the window
        #self.bLogin = True
        #self.bMain = False
        #self.WatchDog()
        

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Danny Browser" % title)
        # method called by the home action

    @pyqtSlot()
    def loadStartedHandler(self):
        print(time.time(), ": load started")

    @pyqtSlot(int)
    def loadProgressHandler(self, prog):
        print(time.time(), ":load progress", prog)

    @pyqtSlot()
    def loadFinishedHandler(self):
        print(time.time(), ": load finished")
        print(self.browser.url())
        print(time.time(), ": load finished")
        if self.bAllowTest:
            if self.bLogin:
                print("navigate_login")
                self.navigate_login()
                self.bLogin = False
                self.bGo5GChange = True
            elif self.bGo5GChange:
                self.Go5GHzSecurity()
                self.bGo5GChange = False
                self.b5GChange = True
            elif not self.bGo5GChange and self.b5GChange:
                self.change5GHzSecurity()
                self.change5GHzChannel_36()
                self.SaveSetting()
                self.b5GChange = False
                self.bClose = True
            elif not self.b5GChange and self.bClose:
                self.close()
        

    def Main(self, bAllowTest=False):
        self.bAllowTest = bAllowTest
        self.browser.setUrl(QUrl("http://10.0.0.1/"))
        #self.Main_Func()

    def Main_Func(self):
        print('navigate_login first')
        self.navigate_login_First()
        print('change password')
        #time.sleep(2)
        #self.changePassword()
        #print('navigate_login')
        #self.navigate_login()
        

    def WatchDog(self):
        Thread(target=self.WatchFunc).start()

    def WatchFunc(self):
        while True:
            if self.brequestF5:
                if self.bLoginFirst: time.sleep(20)
                #pyautogui.press('f5')
                print('reload')
                self.browser.reload()
                print('reload2')
                self.brequestF5 = False
            elif self.bEnter:
                time.sleep(5)
                pyautogui.press('tab')
                pyautogui.press('enter')
                self.bEnter = False
            elif self.bSaveSetting:
                time.sleep(20)
                self.SaveSetting()
                self.bSaveSetting = False
            time.sleep(0.5)

    def get_set_up(self):
        self.browser.page().runJavaScript("document.getElementById('get_set_up').click()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('WiFi_Name').value = 'OBA-WIFI'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('WiFi_Password').value = 'password2'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('button_next').click()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('button_next_01').click()", self.store_value)

    def navigate_login_First(self):
        #self.browser.findText('帳號登入')
        #self.browser.page().runJavaScript("tabLoginModel_OnTabMouseOver(tabInfo['Account'])")
        print('navigate_login first 111')
        #time.sleep(2)
        self.browser.page().runJavaScript("document.getElementById('username').value = 'admin'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('password').value = 'password'", self.store_value)
        print('navigate_login first enter')
        #pyautogui.press('tab')
        #pyautogui.press('enter')
        #time.sleep()
        

        #self.browser.page().runJavaScript("document.getElementByClass('btn').click()", self.store_value)
        #self.bEnter = True
        
    def changePassword(self):
        #self.browser.findText('帳號登入')
        #self.browser.page().runJavaScript("tabLoginModel_OnTabMouseOver(tabInfo['Account'])")

        self.browser.page().runJavaScript("document.getElementById('oldPassword').value = 'password'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('userPassword').value = 'password2'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('verifyPassword').value = 'password2'", self.store_value)
        #time.sleep(2)
        self.browser.page().runJavaScript("document.getElementById('submit_pwd').click()", self.store_value)
        print('change pass')
        #time.sleep(2)
        #pyautogui.press('tab')
        #pyautogui.press('enter')

    def navigate_login(self):
        #self.browser.findText('帳號登入')
        #self.browser.page().runJavaScript("tabLoginModel_OnTabMouseOver(tabInfo['Account'])")

        self.browser.page().runJavaScript("document.getElementById('username').value = 'admin'", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('password').value = 'password2'", self.store_value)
        #time.sleep(2)
        #self.browser.page().runJavaScript("document.getElementByClass('btn').click()", self.store_value)
        print('navigate_login enter')
        #pyautogui.press('tab')
        pyautogui.press('enter')
        #self.change2GHzSecurity()

    #def check_PR_wait(self):
    #    self.browser.setUrl(QUrl("http://evouchers.efoxconn.com/PurchaseRequest/PurchaseRequestList.aspx?status=wait"))

    def Go2GHzSecurity(self):
        self.browser.setUrl(QUrl(self.link2GHz))
        
    def change2GHzSecurity(self):
        print('------------------------')
        self.browser.page().runJavaScript("document.getElementById('network_name').value = 'OBA-WiFi-2.4G'", self.store_value)
        #self.browser.page().runJavaScript("document.getElementById('channel_manual').click()", self.store_value)
        self.browser.page().runJavaScript("showDialog()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('path5').click()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('pop_ok').click()", self.store_value)        
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')
        #self.browser.setUrl(QUrl(self.link5GHz))

    def Go5GHzSecurity(self):
        self.browser.setUrl(QUrl(self.link5GHz)) 

    def change5GHzSecurity(self):
        print('------------------------')
        self.browser.page().runJavaScript("document.getElementById('network_name').value = 'OBA-WiFi-5G'", self.store_value)
        #self.browser.page().runJavaScript("document.getElementById('channel_manual').click()", self.store_value)
        self.browser.page().runJavaScript("showDialog()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('path5').click()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('pop_ok').click()", self.store_value)        
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')
        #self.browser.setUrl(QUrl(self.link5GHz))

    def change5GHzChannel_36(self):
        print('------------------------')
        self.browser.page().runJavaScript("document.getElementById('channel_manual').click()", self.store_value)
        #self.browser.page().runJavaScript("showDialog()", self.store_value)
        self.browser.page().runJavaScript("document.getElementById('channel_number').value = '36'", self.store_value)
        #self.browser.page().runJavaScript("document.getElementById('pop_ok').click()", self.store_value)     
        

    def SaveSetting(self):        
        self.browser.page().runJavaScript("document.getElementById('save_settings').click()", self.store_value)

    def PR_finnish(self):
        self.check_PR_finish()

    def navigate_get(self):
        #self.browser.page().runJavaScript("document.getElementByClassName('content'))", self.store_value)
        try:
            #if self.bGet: self.get_html()
            print(self.browser.url())
        except Exception as e:
            print(e)

    def store_html(self, html):
        self.html = html
        self.toHtmlFinished.emit()

    def get_html(self):
        current_page = self.browser.page()
        current_page.toHtml(self.store_html)
        loop = QEventLoop()
        self.toHtmlFinished.connect(loop.quit)
        loop.exec_()
        content = self.GetContent(self.html,"grdPRList.Data = ","grdPRList.Levels")\
            .strip('\n').replace(';','').replace('[[,','[[').replace('new Date','').replace(',,',',').replace(',[,',',[').strip()
        #print(content)
        #print(type(content))
        lcontent = literal_eval(content)
        #print(lcontent)
        #print(type(lcontent))

        #lcontent = (list(content))
        #print(lcontent)
        if len(lcontent) > 0:
            self.bGet = False
            self.bMain = True
            self.bPRFinish = True
            self.Connect_Server()
        for l in lcontent:
            print(l)
            print('PR Code: ' + l[4])
            print('Waiting for: ' + l[8])
            #self.Send_DB_FinishPR(l)
            self.Send_DB(l)


    def Send_DB(self, NList):
        self.OrdinalNumber = ''
        self.PR_ID = NList[4]
        self.PRCreater = NList[5]
        self.CreatedDate = NList[6][1]
        self.ProcessStatus = NList[7]
        self.Processer = NList[8]
        self.Last_Transaction = NList[9][1]
        self.Amount = NList[10]

        #cmd = "EXEC usp_Pendingprlist_Insert @PrId=" + self.PR_ID + ",@PRCreater=" + self.PRCreater + ",@CreatedDate=" + self.CreatedDate + ",@ProcessStatus=" + self.ProcessStatus + ",@Processer=" + self.Processer + ",@LastTransaction=" + self.Last_Transaction + ",@Amount=" + self.Amount
        #cmd = 'INSERT INTO PENDINGPRLIST(PR_ID, PRCreater, CreatedDate, ProcessStatus, Processer, Last_Transaction, Amount, WorkingDate)' \
        #      'VALUES('', '', '', '', '', '', '', '')'
        values = "'" + self.PR_ID + "', N'" + self.PRCreater + "', '" + self.CreatedDate + "', N'" + self.ProcessStatus + "', N'" + self.Processer +\
                 "', '" + self.Last_Transaction + "', '" + self.Amount + "', '" + (datetime.now().__format__('%d-%B-%Y %H:%M:%S'))+"'"
        #values = "@PrId='" + self.PR_ID + "', @PRCreater=N'" + self.PRCreater + "', @CreatedDate='" + self.CreatedDate + "', @ProcessStatus=N'" + self.ProcessStatus + "', @Processer=N'" + self.Processer + "', @LastTransaction='" + self.Last_Transaction + "', @Amount='" + self.Amount + "'"
        cmd = "INSERT INTO PENDINGPRLIST(PR_ID, PRCreater, CreatedDate, ProcessStatus, Processer, Last_Transaction, Amount, WorkingDate) VALUES(" + values + ")"
        #cmd = "EXEC usp_Pendingprlist_Insert " + values
        print(cmd)
        self.get_data()
        self.cursor.execute(cmd)
        self.cursor.commit()
        print('=======================')
        self.get_data()

    def Send_DB_FinishPR(self, NList):
        self.OrdinalNumber = ''
        self.PR_ID = NList[4]
        self.PRCreater = NList[5]
        self.CreatedDate = NList[6][1]
        self.ProcessStatus = NList[7]
        self.Processer = NList[8]
        self.Last_Transaction = NList[9][1]
        self.Amount = NList[10]

        #cmd = "EXEC usp_Pendingprlist_Insert @PrId=" + self.PR_ID + ",@PRCreater=" + self.PRCreater + ",@CreatedDate=" + self.CreatedDate + ",@ProcessStatus=" + self.ProcessStatus + ",@Processer=" + self.Processer + ",@LastTransaction=" + self.Last_Transaction + ",@Amount=" + self.Amount
        #cmd = 'INSERT INTO PENDINGPRLIST(PR_ID, PRCreater, CreatedDate, ProcessStatus, Processer, Last_Transaction, Amount, WorkingDate)' \
        #      'VALUES('', '', '', '', '', '', '', '')'
        values = "'" + self.PR_ID + "', N'" + self.PRCreater + "', '" + self.CreatedDate + "', N'" + self.ProcessStatus + "', N'" + self.Processer +\
                 "', '" + self.Last_Transaction + "', '" + self.Amount + "', '" + (datetime.now().__format__('%d-%B-%Y %H:%M:%S'))+"'"
        #values = "@PrId='" + self.PR_ID + "', @PRCreater=N'" + self.PRCreater + "', @CreatedDate='" + self.CreatedDate + "', @ProcessStatus=N'" + self.ProcessStatus + "', @Processer=N'" + self.Processer + "', @LastTransaction='" + self.Last_Transaction + "', @Amount='" + self.Amount + "'"
        cmd = "INSERT INTO FINISHPRLIST(PR_ID, PRCreater, CreatedDate, ProcessStatus, Processer, Last_Transaction, Amount, WorkingDate) VALUES(" + values + ")"
        #cmd = "EXEC usp_Pendingprlist_Insert " + values
        print(cmd)
        self.get_data()
        self.cursor.execute(cmd)
        self.cursor.commit()
        print('=======================')
        self.get_data()

    def get_data(self):
        self.maillist = []
        self.cursor.execute("SELECT PR_ID FROM PENDINGPRLIST")
        # print(self.maillist)
        # print(self.maillist[1])
        for row in self.cursor:
            self.maillist.extend(row)
            # print(row[0].split(','))
        print(self.maillist)

    def Connect_Server(self):
        print('Connect_Server')
        server = '10.228.110.91'
        database = 'TOOLROOM'
        username = 'toolroom'
        password = 'Foxconn123#'
        self.cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.cnxn.cursor()
        time.sleep(10)
        #print(self.cnxn)

    def GetContent(self, buf, strstart, strend):
        # strresult="none"
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult


    def navigate_home(self):
        self.browser.setUrl(QUrl("http://evouchers.efoxconn.com/LoginPage.aspx?ReturnUrl=%2fdefault.aspx"))

    def store_value(self, param):
        self.value = param
        print("Param: " + str(param))

    # method called by the line edit when return key is pressed

    def navigate_to_url(self):
        # getting url and converting it to QUrl objetc
        q = QUrl(self.urlbar.text())

        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("http")

            # set the url to the browser
        self.browser.setUrl(q)

        # method for updating url

    # this method is called by the QWebEngineView object
    def update_urlbar(self, q):
        # setting text to the url bar
        self.urlbar.setText(q.toString())

        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)

    # creating a pyQt5 application

    def Start(self):
        Thread(target=self.navigate_login).start()
        time.sleep(20)
        Thread(target=self.check_PR_wait).start()
        time.sleep(5)
        Thread(target=self.navigate_get).start()


app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Danny Browser")

# creating a main window object
window = MainWindow()

# loop
app.exec_()

'''self.maillist = []
self.cursor.execute("SELECT PR_ID FROM PENDINGPRLIST")
# print(self.maillist)
# print(self.maillist[1])
for row in self.cursor:
   self.maillist.extend(row)
   # print(row[0].split(','))
print(self.maillist)'''
