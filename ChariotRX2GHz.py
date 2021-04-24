import os
import subprocess
from threading import Thread


class MainChariotRX2GHz():
    def __init__(self, ichariotpath=r'D:\Test_Program\Ixia\IxChariot', itstpath='\\Tests\\WF2GRX.tst', ifmttst='\\Tests\\WF2GRX.tst', **kargs):
        self.buffer = ''
        self.ip1 = ''
        self.ip2 = ''
        self.chariotpath = ichariotpath
        self.itstpath = itstpath
        self.ifmttst = ifmttst
        temp_dir_df = self.chariotpath
        if not os.path.isdir(temp_dir_df):
            os.mkdir(temp_dir_df)
        self.testpath = ''
        self.RunChariot()

    def GetContent(self, buf, strstart, strend):
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult

    def RunChariot(self):
        print('Running..')
        self.Call_runtst()
        self.Call_fmttst()
        tResult = self.GetContent(self.buffer, 'THROUGHPUT', 'TRANSACTION RATE')
        print('\n\ntResult: '+tResult)
        iResult = self.GetContent(tResult, 'Totals:   ', ' ')
        print('\n\niResult: '+iResult+'(Mbps)^-^')

    def Call_runtst(self):
        CREATE_NO_WINDOW = 0X08000000
        #cmd = self.chariotpath + '\\runtst.exe Tests\\test1.tst'# -t 20 -v
        cmd = self.chariotpath + '\\runtst.exe ' + self.chariotpath + self.itstpath
        print(cmd)
        p = subprocess.Popen(cmd, stdin= subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.chariotpath, bufsize=1, creationflags=CREATE_NO_WINDOW)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            self.buffer += res
            if res.strip() != '':
                print(res)
            if not line: break
        p.stdout.close()
        p.wait()

    def Call_fmttst(self):
        CREATE_NO_WINDOW = 0X08000000
        cmd = self.chariotpath + '\\fmttst.exe ' + self.chariotpath + self.ifmttst
        print(cmd)
        p = subprocess.Popen(cmd, stdin= subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.chariotpath, bufsize=1, creationflags=CREATE_NO_WINDOW)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            self.buffer += res
            if res.strip() != '':
                print(res)
            if not line: break
        p.stdout.close()
        p.wait()
        

if __name__=='__main__':
    MainChariotRX2GHz()
