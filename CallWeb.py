import importlib
import time

def Get_Setup():
    print('--------START Get_Setup')
    from VDTweb import Get_Setup

def Login_First():
    from VDTweb import Login_First

def Login():
    from VDTweb import Login

def Check_Info(firsttest):
    print('--------START GetInfo')
    if firsttest == 0:
        from VDTweb import GetInfo
    else:
        #importlib.reload(Get_Setup)
        from VDTweb import GetInfo
    del GetInfo

def WiFi24GHz():
    from VDTweb import WiFi24GHz

def WiFi5GHz():
    from VDTweb import WiFi5GHz

for i in range(0, 20):
    Check_Info(i)
    time.sleep(3)
