import os
import subprocess
from threading import Thread
import time


class App():
    def __init__(self, master=None):        
        print('Main')
        self.Main_OBA_WiFi()
        
    def Main_OBA_WiFi(self):
        '''for i in range(0, 10):
            i += 1
            print(i)
            time.sleep(0.5)
            if i == 9:                
                self.Get_Setup()
                break
            
        for i in range(0, 50):
            i += 1
            print(i)
            time.sleep(1)
            if i == 49:
                self.Login_First()
                break'''
        for i in range(0, 30):
            i += 1
            print(i)
            time.sleep(1)
            if i == 9:                
                Thread(target=self.WiFi5GHz36).start()
            elif i == 29:                
                Thread(target=self.WiFi5GHz48).start()
                

    def Get_Setup(self):
        from VDTweb import Get_Setup

    def Login_First(self):
        from VDTweb import Login_First

    def Login(self):
        from VDTweb import Login

    def WiFi24GHz(self):
        from VDTweb import WiFi24GHz

    def WiFi5GHz36(self):
        from VDTweb import WiFi5GHz36

    def WiFi5GHz48(self):
        from VDTweb import WiFi5GHz48        
    

if __name__=='__main__':
    App()
