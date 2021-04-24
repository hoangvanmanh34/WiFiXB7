import os
import subprocess
import socket
import time
from ast import literal_eval
from datetime import datetime
from threading import Thread

class App():
    def __init__(self):
        print('@Danny_2021:ver1.0')
        print('START:')
        itimestart = datetime.now()
        print(itimestart)
        idata = '@Danny_2021:ver1.0\nSTART:' + str(itimestart) + '\n'
        self.SaveLog(idata)
        self.Open_SelfServer()

    def Open_SelfServer(self):
        print('start')
        self.serversocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.200.2'#socket.gethostname()
        port = 65432
        self.serversocket.bind((host,port))

        self.serversocket.listen(5)
        connect=True
        while True:
            self.conn,self.client=self.serversocket.accept()
            try:
                    print('connection from: ',self.client)
                    #while self.conn:
                    infodata=self.conn.recv(1024).decode()
                    print(type(infodata))
                    idatalist = literal_eval(infodata)
                    print('receive from client: ',infodata)
                    itimestart = datetime.now()
                    print(itimestart)
                    self.SaveLog(str(itimestart) + str(infodata)+'\n')
                    irequest = idatalist[0]
                    icommand = idatalist[1]
                    print(irequest)
                    print(icommand)
                    if irequest.upper() == 'CONNECT':
                        self._Connect(icommand)
                    if irequest.upper() == 'DISCONNECT':
                        self._Disconnect(icommand)
                    ifeedback = 'REQUEST:DONE^-^'
                    self.conn.sendall(ifeedback.encode())
                    '''a=Find_Password(data)
                    if a:
                        print('response to client: ',a)
                        conn.sendall(a.encode())
                    else:
                        print('no data')'''
                    
            except Exception as e:
                print(e)

    def _Connect(self, issid):
        itimestart = datetime.now()
        print(itimestart)
        cmd = "netsh wlan connect ssid=" + str(issid) + " name=" + str(issid)#r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetSetup\GetSetup.exe"
        buffer = ''
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            print(res)
            if not line: break
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        #return False

    def _Disconnect(self, issid):
        itimestart = datetime.now()
        print(itimestart)
        cmd = "netsh wlan connect ssid=" + str(issid) + " name=" + str(issid)#r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetSetup\GetSetup.exe"
        buffer = ''
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            print(res)
            if not line: break
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        #return False

    
    def GetContent(self,buf, strstart, strend):
        # strresult="none"
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult

    def SaveLog(self, ilog):
        try:
            datetosave = str(datetime.now().__format__('%d-%B-%Y'))
            timetosave = str(datetime.now().__format__('%d-%B-%Y_%H-%M-%S'))
            full_savedir = 'D:/Logs/Golden/'+datetosave
            if not os.path.isdir(full_savedir): os.makedirs(full_savedir)
            log_file = open(full_savedir + '/_' + timetosave + '.txt', 'a')
            log_file.write(ilog)
            log_file.close()    
        except Exception as e:
            print('save log fail')
            print(e)

App()
