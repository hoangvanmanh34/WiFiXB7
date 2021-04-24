import os
import subprocess
from threading import Thread
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import imutils
import numpy as np
from tkinter import *
from tkinter import messagebox
from win32api import GetSystemMetrics
import socket
from ast import literal_eval
import hashlib
import json
from datetime import datetime
import serial
import serial.tools.list_ports
import Serial_COM
import importlib
#from VDTweb import CallWeb
#import Chariot


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.window = master
        # --------------------------------------------
        self.TesterName = socket.gethostname()
        self.TesterIP = socket.gethostbyname(socket.gethostname())
        self.Screen_Width = GetSystemMetrics(0)
        self.Screen_Height = GetSystemMetrics(1)
        self.logwidth = int(self.Screen_Width / 3 - 20)
        self.logheight = int(self.Screen_Height / 3 - 20)
        self.cwidth = int(self.Screen_Width / 2)
        self.cheight = int(self.Screen_Height / 3 * 2)
        self.dut_width_rate = 1280 / 800
        self.dut_height_rate = 800 / 500
        # --------------------------------------------
        self.bPress = False
        self.bstart = False
        self.Test_Flag = False
        self.bstart_test = False
        self.bend_test = False
        self.bCheck_DUT_Alive = True
        self.iAllowTest = False
        self.allowListen = False
        self.Final_Result = False
        self.bconnected = False
        # --------------------------------------------
        self.countTime = 0
        self.TimeOut = 951
        self.first_Get_Setup = 0
        self.first_Check_Info = 0
        self.cpass=0
        self.cfail=0
        self.i2GHzTXvalue = None
        self.i2GHzRXvalue = None
        self.i5GHzTXvalue = None
        self.i5GHzRXvalue = None
        self.i6GHzTXvalue = None
        self.i6GHzRXvalue = None
        # --------------------------------------------
        self.vFPY = StringVar(root)
        self.vFPY.set('NA')
        self.vTotal = IntVar(root)
        self.vTotal.set(0)
        self.vPass = IntVar(root)
        self.vPass.set(0)
        self.vFail = IntVar(root)
        self.vFail.set(0)
        self.vDUTSN = StringVar(root)
        self.vDUTSN.set('-')
        self.vMODEL = StringVar(root)
        self.vMODEL.set('-')
        # --------------------------------------------
        self.iSerial = Serial_COM.Serial_COM()
        self.bsfclive = True
        self.iSendSFC = ''
        self.isfcOpen = False
        self.SFCInfoOK = False
        self.DUT_IP = ''
        self.WF24GHzIP = ''
        self.WF5GHzIP = ''
        self.WF6GHzIP = ''
        self.DUT_SN_Length = 18
        self.Error_code = 'No error'
        # --------------------------------------------
        self.infodata = ''
        self.DUTSN = ''
        # --------------------------------------------        
        self.iKfuncName = ''
        self.iKitimeout = 0
        # --------------------------------------------
        #self.grid()
        # self.master.rowconfigure(100, weight=1)
        # self.master.columnconfigure(10, weight=1)
        Frame.__init__(self, master)
        #self.grid()
        self.PC_Name = socket.gethostname()
        self.PC_IP_Addr = socket.getaddrinfo(socket.gethostname(), None)
        self.master.title("OBA_WiFi.     @Danny_2021")
        self.tStyle = ttk.Style()
        #self.tStyle.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        #self.tStyle.configure('green.Horizontal.TProgressbar', foreground='green', background='green')
        # print(self.tStyle.theme_names())
        self.tStyle.configure("Custom.Treeview.Heading", foreground='blue', background='blue')
        tabControl = ttk.Notebook(root)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Main')
        tabControl.add(tab2, text='Config')
        tabControl.pack(expand=1, fill="both")
        # ---------------------------------------------------------------------
        self.master.rowconfigure(13, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.Frame1 = Frame(tab1)#, bg="lightskyblue"
        self.Frame1.grid(row=0, column=0, sticky=W + E + N + S, pady=0, padx=5)
        self.Frame2 = Frame(tab1)
        self.Frame2.grid(row=1, column=0, sticky=W + E + N + S, pady=10, padx=0)
        self.Frame3 = Frame(tab1, bg="white")
        self.Frame3.grid(row=2, column=0, sticky=W + E + N + S, pady=0, padx=5)
        self.Frame4 = Frame(tab1)
        self.Frame4.grid(row=3, rowspan=10, column=1, columnspan=5, sticky=W + E + N + S, pady=10, padx=5)
        # ------------------------------------------------------------------------
        self.Frame5 = Frame(tab2)#, bg="lightskyblue"
        self.Frame5.grid(row=0, column=0, sticky=W + E + N + S, pady=0, padx=5)
        self.Frame6 = Frame(tab2)
        self.Frame6.grid(row=1, column=0, sticky=W + E + N + S, pady=10, padx=0)
        # -------create user interface--------------------------------------------------
        menuBar = Menu(self.master)
        self.master.config(menu=menuBar)
        self.fileMenu = Menu(menuBar, tearoff=0)
        self.fileMenu.add_command(label="Start", command=self.Main)
        self.fileMenu.add_separator()        
        self.fileMenu.add_command(label="Stop", command=self._stop_Test)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Reset Beach", command=self._reset_Beach)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Configure", command=None)
        self.fileMenu.add_separator()
        menuBar.add_cascade(label="File", menu=self.fileMenu)        
        # ---------------------------------------------
        #        ********MAIN TAB
        # ---------------------------------------------
        self.lbStation = tk.Label(self.Frame1, text='OBA WiFi', borderwidth=4, font='serif 25',
                                  width=14, height=2, bg='white', fg='black')
        self.lbStation.grid(row=0, rowspan = 2, column=0, sticky=E, padx=0, pady=5)
        # --------------------------------------------
        self.lbStatus = tk.Label(self.Frame1, text='STANDBY', borderwidth=4, font='serif 25',
                                 width=28, height=2,
                                 bg='white', fg='blue')
        self.lbStatus.grid(row=0, rowspan = 2, column=1, columnspan=2, sticky=W, padx=5, pady=5)
        # -------------------------------------------
        self.lbTime = tk.Label(self.Frame1, text='TIME', borderwidth=4, font='serif 25',
                                  width=10, height=2, bg='white', fg='black')
        self.lbTime.grid(row=0, rowspan = 2, column=3, sticky=E, padx=5, pady=5)
        # -------------------------------------------
        self.lbTesterName = tk.Label(self.Frame1, text=self.TesterName, borderwidth=0, font='serif 25',
                                  width=15, height=1, bg='white', fg='black')
        self.lbTesterName.grid(row=0, column=4, sticky=E, padx=5, pady=5)        
        # -------------------------------------------
        self.lbTesterIP = tk.Label(self.Frame1, text=self.TesterIP, borderwidth=0, font='serif 25',
                                  width=15, height=1, bg='white', fg='black')
        self.lbTesterIP.grid(row=1, column=4, sticky=E, padx=5, pady=5)
        # -------------------------------------------
        self.sfclog = Text(self.Frame1, height=5, width=100, font='serif 11')
        self.sfclog.grid(row=2, rowspan=2, column=0, columnspan=2, sticky=W, pady=5)
        scrollbl = Scrollbar(self.Frame1, command=self.sfclog.yview)
        scrollbl.grid(row=2, rowspan=2, column=2, sticky='nsew', pady=5)
        self.sfclog['yscrollcommand'] = scrollbl.set
        # -------------------------------------------
        self.lbDUTSN = tk.Label(self.Frame1, textvariable=self.vDUTSN, borderwidth=0, font='serif 25',
                                  width=26, height=1, bg='blue', fg='white')
        self.lbDUTSN.grid(row=2, column=3, columnspan=3, sticky=E, padx=5, pady=5)        
        # -------------------------------------------
        self.lbMODEL = tk.Label(self.Frame1, textvariable=self.vMODEL, borderwidth=0, font='serif 25',
                                  width=26, height=1, bg='blue', fg='white')
        self.lbMODEL.grid(row=3, column=3, columnspan=3, sticky=E, padx=5, pady=5)
        # -------------------------------------------
        '''self.lbTime = tk.Label(self.Frame1, text='TIME', borderwidth=4, font='serif 25',
                               width=10, height=2,
                               bg='white', fg='black')
        self.lbTime.grid(row=0, column=2, sticky=W, padx=5, pady=5)'''
        # --------------------------------------------
        #self.canvas = Canvas(self.Frame2, width=self.cwidth + 25, height=self.cheight)
        #self.canvas.grid(row=0, rowspan=10, column=0, columnspan=4, sticky=W + E + N + S, padx=5)
        #self.canvas.bind("<Double-Button-1>", self.Canvas_Left_Click)
        #self.canvas.bind("<ButtonRelease-3>", self.Right_Canvas_Button_Release)
        #self.canvas.bind("<Button-1>", self.Store_Mouse_Click)
        #self.canvas.bind("<Button-3>", self.Right_Store_Mouse_Click)
        #self.canvas.bind("<ButtonRelease-1>", self.Canvas_Button_Release)
        # --------------------------------------------
        # self.lbspace1 = tk.Label(self.Frame3, text='    ', borderwidth=4, font='serif 14', fg='black')
        # self.lbspace1.grid(row=0, column=0, sticky=W)
        # self.lbspace2 = tk.Label(self.Frame3, text='   ', borderwidth=4, font='serif 14', fg='black')
        # self.lbspace2.grid(row=2, column=0, sticky=W)
        # self.progress_bar = ttk.Progressbar(self.Frame3, orient="horizontal", mode="determinate", maximum=40, value=0,
        #                                     length=400)
        # self.progress_bar.grid(row=1, rowspan=2, column=0, sticky=W)

        # ---------------------------------------------
        datalabels = ('Date', 'Result', 'Model', 'SN', 'WiFi', 'Channel', 'TX', 'RX')
        self.DataList = ttk.Treeview(self.Frame2, columns=datalabels, show='headings', height=18, style="Custom.Treeview")
        for col in datalabels:
            self.DataList.heading(col, text=col)
            if col == 'Date' or col == 'SN':
                self.DataList.column(column=col, width=140, anchor="center")
            else:
                self.DataList.column(column=col, width=90, anchor="center")
        self.DataList.grid(row=0, column=0, sticky=W, pady=5, padx=5)
        '''for i in range(0, 25):
            idatetime = str(datetime.now().__format__('%d-%B-%Y'))+'   '+str(datetime.now().__format__('%H:%M:%S'))
            self.DataList.insert("", "0", values=(idatetime, "PASS", "U46C420.00", "SN012345678", "2.4GHz", i, 530, 590))'''
        # ---------------------------------------------
        self.log = Text(self.Frame2, height=24, width=72, font='serif 10', bg='lightgray')
        self.log.grid(row=0, column=1, sticky=W, pady=5)
        scrollb = Scrollbar(self.Frame2, command=self.log.yview)
        scrollb.grid(row=0, column=2, sticky='nsew', pady=5)
        self.log['yscrollcommand'] = scrollb.set
        self.log.see(END)
        #scrollbx = Scrollbar(self.Frame2, command=self.log.xview)
        #scrollbx.grid(row=1, column=1, sticky='nsew', pady=5)
        #self.log['xscrollcommand'] = scrollbx.set
        # ---------------------------------------------
        '''fpylabels = ('TOTAL', 'PASS', 'FAIL', 'FPY')
        self.FPYList = ttk.Treeview(self.Frame2, columns=fpylabels, show='headings', height=2, style="Custom.Treeview")
        for col in fpylabels:
            self.FPYList.heading(col, text=col)
            self.FPYList.column(column=col, width=90, anchor="center")
        self.FPYList.grid(row=1, column=0, sticky=W, pady=5, padx=5)
        self.FPYList.insert("", "0", values=(1000, 500, 500, 1000/500))'''
        # ---------------------------------------------
        self.lbTotal = tk.Label(self.Frame3, text='||    TOTAL:', borderwidth=2, font='serif 15',
                                  width=11, height=1, bg='black', fg='white')
        self.lbTotal.grid(row=0, column=0, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalValue = tk.Label(self.Frame3, textvariable=self.vTotal, borderwidth=2, font='serif 15',
                                  width=5, height=1, bg='white', fg='black')
        self.lbTotalValue.grid(row=0, column=1, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalPass = tk.Label(self.Frame3, text='||    PASS:', borderwidth=2, font='serif 15',
                                  width=11, height=1, bg='black', fg='white')
        self.lbTotalPass.grid(row=0, column=2, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalPassValue = tk.Label(self.Frame3, textvariable=self.vPass, borderwidth=2, font='serif 15',
                                  width=5, height=1, bg='white', fg='black')
        self.lbTotalPassValue.grid(row=0, column=3, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalFail = tk.Label(self.Frame3, text='||    FAIL:', borderwidth=0, font='serif 15',
                                  width=11, height=1, bg='black', fg='white')
        self.lbTotalFail.grid(row=0, column=4, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalFailValue = tk.Label(self.Frame3, textvariable=self.vFail, borderwidth=0, font='serif 15',
                                  width=5, height=1, bg='white', fg='black')
        self.lbTotalFailValue.grid(row=0, column=5, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalFPY = tk.Label(self.Frame3, text='||    FPY:', borderwidth=0, font='serif 15',
                                  width=11, height=1, bg='black', fg='white')
        self.lbTotalFPY.grid(row=0, column=6, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.lbTotalFPYValue = tk.Label(self.Frame3, textvariable=self.vFPY, borderwidth=0, font='serif 15',
                                  width=8, height=1, bg='green', fg='white')
        self.lbTotalFPYValue.grid(row=0, column=7, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        self.progress_bar = ttk.Progressbar(self.Frame3, orient="horizontal", mode="determinate", maximum=100, value=0, length=400)
        self.progress_bar.grid(row=0, rowspan=2, column=8, sticky=E, padx=80)
        # ---------------------------------------------
        #        ********CONFIG TAB
        # ---------------------------------------------
        self.btnOpenCOM = tk.Button(self.Frame5, text="SFC_Closed", fg='white', bg='red', font='serif 12',
                                    width=17, command=self.COM_Control)
        self.btnOpenCOM.grid(row=0, column=0, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
            self.vconnected = StringVar(root)
        self.vconnected.set("COM_Port")
        lconnected = OptionMenu(self.Frame5, self.vconnected, *connected)
        lconnected.config(width=28)
        lconnected.grid(row=0, column=1, padx=5)
        # ---------------------------------------------
        self.lbcfgDUTIP = tk.Label(self.Frame5, text='DUT IP', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgDUTIP.grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgDUTIP = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgDUTIP.grid(row=1, column=1, sticky=W, pady=5)
        # ---------------------------------------------
        self.lbcfgWF24GHzIP = tk.Label(self.Frame5, text='WiFi 2.4GHz IP', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF24GHzIP.grid(row=2, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF24GHzIP = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF24GHzIP.grid(row=2, column=1, sticky=W, pady=5)
        # ---------------------------------------------        
        self.lbcfgWF5GHzIP = tk.Label(self.Frame5, text='WiFi 5GHz IP', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF5GHzIP.grid(row=3, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF5GHzIP = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF5GHzIP.grid(row=3, column=1, sticky=W, pady=5)
        # ---------------------------------------------
        self.lbcfgWF6GHzIP = tk.Label(self.Frame5, text='WiFi 6GHz IP', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF6GHzIP.grid(row=4, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF6GHzIP = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF6GHzIP.grid(row=4, column=1, sticky=W, pady=5)
        # ---------------------------------------------
        self.lbcfgWF24GHz_SSID = tk.Label(self.Frame5, text='WiFi 2.4GHz SSID', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF24GHz_SSID.grid(row=5, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF24GHz_SSID = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF24GHz_SSID.grid(row=5, column=1, sticky=W, pady=5)
        # ---------------------------------------------        
        self.lbcfgWF5GHz_SSID = tk.Label(self.Frame5, text='WiFi 5GHz SSID', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF5GHz_SSID.grid(row=6, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF5GHz_SSID = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF5GHz_SSID.grid(row=6, column=1, sticky=W, pady=5)
        # ---------------------------------------------
        self.lbcfgWF6GHz_SSID = tk.Label(self.Frame5, text='WiFi 6GHz SSID', borderwidth=2, font='serif 15',
                                  width=15, height=1, bg='black', fg='white')
        self.lbcfgWF6GHz_SSID.grid(row=7, column=0, sticky=E, padx=5, pady=5)
        self.txtcfgWF6GHz_SSID = Text(self.Frame5, height=1, width=20, font='serif 15', bg='lightgray')
        self.txtcfgWF6GHz_SSID.grid(row=7, column=1, sticky=W, pady=5)
        # ---------------------------------------------
        self.btnSaveCFG = tk.Button(self.Frame5, text="Save IP", fg='white', bg='Blue', font='serif 12',
                                    width=42, command=self.Save_CFG)
        self.btnSaveCFG.grid(row=8, column=0, columnspan=2, sticky=E, padx=5, pady=5)
        # ---------------------------------------------
        #Thread(target=self.Open_SelfServer).start()
        #self._callWebTool = CallWeb.CallWebTool()
        #self.fChariot = Chariot.MainChariot(r'C:\Program Files (x86)\Ixia\IxChariot')
        self.vMODEL.set('MODEL: U46C420.00')
        #self.Main_WiFi()

    def Main(self):
        print('Start')
        self.DUT_IP = self.txtcfgDUTIP.get(1.0, END).strip()
        self.WF24GHzIP = self.txtcfgWF24GHzIP.get(1.0, END).strip()
        self.WF5GHzIP = self.txtcfgWF5GHzIP.get(1.0, END).strip()
        self.WF6GHzIP = self.txtcfgWF6GHzIP.get(1.0, END).strip()
        
        self.WiFi24GHz_SSID = self.txtcfgWF24GHz_SSID.get(1.0, END).strip()
        self.WiFi5GHz_SSID = self.txtcfgWF5GHz_SSID.get(1.0, END).strip()
        self.WiFi6GHz_SSID = self.txtcfgWF6GHz_SSID.get(1.0, END).strip()
        print(self.DUT_IP)
        print(self.WF24GHzIP)
        print(self.WF5GHzIP)
        print(self.WF6GHzIP)
        
        print(self.WiFi24GHz_SSID)
        print(self.WiFi5GHz_SSID)
        print(self.WiFi6GHz_SSID)
        if not self.bstart:
            self.Reset_Status()
            #self._SFC_Control()            
            self.bstart = True
            self.Test_Flag = True
            Thread(target=self.Test_Time).start() 
            Thread(target=self.Self_test).start()            
            '''if result:
                self.lbStatus.configure(text='PASS', fg='blue')
                self.log.insert(END, '-->PASS\r\n')
            else:
                self.lbStatus.configure(text='FAIL', fg='red')
                self.log.insert(END, '-->FAIL\r\n')
                self.Test_Flag = False'''

    def _stop_Test(self):
        self.Test_Flag = False

    def _reset_Beach(self):
        self.Test_Flag = False
        self.sfclog.delete(1.0, END)
        self.log.delete(1.0, END)
        self.lbTime.config(text='TIME')
        self.lbStatus.config(text='STANDBY', fg='blue', bg='white')
        #self.log.insert(END, str(self.TesterName) + ':'+str(self.TesterIP) + '\n')
        for i in self.DataList.get_children():
            self.DataList.delete(i)
        self.vTotal.set(0)
        self.vPass.set(0)
        self.vFail.set(0)
        self.vFPY.set('NA')
        self.lbTotalFPYValue.config(bg='green')
    
    def Reset_Status(self):
        self.Test_Flag = False
        self.iAllowTest = False
        self.DUTSN = 'No SN'
        self.sfclog.delete(1.0, END)
        self.log.delete(1.0, END)
        self.lbTime.config(text='TIME')
        self.lbStatus.config(text='STANDBY', fg='blue')
        self.lbDUTSN.config(text='-')
        self.lbMODEL.config(text='-')
        self.log.insert(END, str(self.TesterName) + ':'+str(self.TesterIP) + '\n')

    def _FPY_Func(self):
        Thread(target=self.FPY_Func).start()
        

    def FPY_Func(self):
        self.vTotal.set(self.cpass+self.cfail)
        self.vPass.set(self.cpass)
        self.vFail.set(self.cfail)
        if self.vTotal.get() == 0:
            self.vFPY.set('NA')
            self.lbTotalFPYValue.config(bg='green')
        else:
            FPYvalue = round(self.vPass.get()/self.vTotal.get()*100, 2)
            self.vFPY.set(str(FPYvalue) + '%')
            iFPYvalue = self.vFPY.get()
            if FPYvalue < 50:
                self.lbTotalFPYValue.config(bg='red')
        print(FPYvalue)
        return iFPYvalue


    def Main_WiFi(self):
        '''if not self._WiFi24GHz_1(): return False
        self.Update_Progress(50, itheme='default', istyle='green')
        if not self._WiFi24GHz_6(): return False
        self.Update_Progress(60, itheme='default', istyle='green')
        if not self._WiFi24GHz_11(): return False
        self.Update_Progress(70, itheme='default', istyle='green')
        if not self._WiFi5GHz_36(): return False
        self.Update_Progress(80, itheme='default', istyle='green')
        if not self._WiFi5GHz_48(): return False
        self.Update_Progress(85, itheme='default', istyle='green')
        if not self._WiFi5GHz_153(): return False
        self.Update_Progress(90, itheme='default', istyle='green')'''
        if not self._Reset_Factory_RTD(): return False
        return True

    def _Get_Setup(self):
        itimestart = datetime.now()
        print(itimestart)
        cmd = r"D:\Test_Program\OBA_WIFI\GetSetup\GetSetup.exe"#r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetSetup\GetSetup.exe"
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        self._Kill_Process('GetSetup.exe', 35)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
            iResult = self.GetContent(buffer, '-Result:', '^-^') 
            if iResult == 'PASS_SETUP' or iResult == 'GO_INDEX_LINK':
                #time.sleep(30)
                killcmd = 'taskkill /f /im GetSetup.exe'
                os.system(killcmd)
                itimeend = datetime.now()
                print(itimeend)
                return True
        itimeend = datetime.now()
        print(itimeend)
        #p.stdout.close()
        #p.wait()
        return False

    def _Login_First(self):
        itimestart = datetime.now()
        print(itimestart)
        cmd = r"D:\Test_Program\OBA_WIFI\Login_First\Login_First.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\Login_First\Login_First.exe"
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        self._Kill_Process('Login_First.exe', 15)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break            
            iResult = self.GetContent(buffer, '-Result:', '^-^')  
            if iResult == 'PASS_CHANGED' or iResult == 'HAS_CHANGED':
                #time.sleep(5)
                killcmd = 'taskkill /f /im Login_First.exe'
                os.system(killcmd)
                return True
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        return False

    def _Check_Info(self):
        itimestart = datetime.now()
        print(itimestart)
        cmd = r"D:\Test_Program\OBA_WIFI\GetInfo\GetInfo.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetInfo\GetInfo.exe"
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        iDUTSN = self.GetContent(buffer, '-Serial Number:', '^-^')
        print('-Request DUT_SN_Length:' + str(self.DUT_SN_Length))
        print('-Get DUT_SN_Length:' + str(iDUTSN))
        if len(iDUTSN) == self.DUT_SN_Length:
            self.DUTSN = iDUTSN
            self.vDUTSN.set(iDUTSN)
            return True
        return False

    def _Reset_Factory_RTD(self):   
        print('-----START RTD-----')     
        if not self._Factory_RTD():
            self.Error_code = 'RTD001'
            return False
        self.Update_Progress(95, itheme='default', istyle='green')
        time.sleep(200)
        if not self._Check_Factory_RTD(): 
            self.Error_code = 'RTD001'
            return False
        self.Update_Progress(100, itheme='default', istyle='green')
        return True

    def _Factory_RTD(self):
        itimestart = datetime.now()
        print(itimestart)
        cmd = r"D:\Test_Program\OBA_WIFI\RTFD\RTFD.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\RTFD\RTFD.exe"
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        iResult = self.GetContent(buffer, '-iResult:', '^-^')  
        print('-RTD Result:' + str(iResult))
        if iResult == 'LOGOUT_RTD':
            return True
        return False

    def _Check_Factory_RTD(self):
        itimestart = datetime.now()
        print(itimestart)
        cmd = r"D:\Test_Program\OBA_WIFI\CheckRTD\CheckRTD.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\CheckRTD\CheckRTD.exe"
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
        itimeend = datetime.now()
        print(itimeend)
        p.stdout.close()
        p.wait()
        iResult = self.GetContent(buffer, '-Result:', '^-^')  
        print('-RTD Result:' + str(iResult))
        if iResult == 'PASS_RTD':
            return True
        return False

    def _Test_Throughput(self, ipath):
        try:
            cmd2 = ipath
            print(cmd2)
            buffer = ''
            p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p2.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                #self.log.insert(END,res)
                #self.log.see(END)
                if not line: break
            self.log.insert(END,buffer)
            self.log.see(END)
            p2.stdout.close()
            p2.wait()
            iRESULT = float(self.GetContent(buffer, 'iResult: ', '(Mbps)^-^').replace(',', ''))
            return iRESULT 
        except Exception as e:
            print(e)
            self.log.insert(END,e)
            return False

    def _WiFi24GHz_1(self):
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi24GHz1\WiFi24GHz1.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi24GHz1\WiFi24GHz1.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********2.4GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 1 TX'):
                    bcheckping = True
                    break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI1'
                return False
            TX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX2GHz\ChariotTX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX2GHz\ChariotTX2GHz.exe")
            self.i2GHzTXvalue = TX2GRESULT
            if TX2GRESULT < 100:
                self.Error_code = 'WF2TXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 1, TX2GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 1, TX2GRESULT, None)
            # --------------------------------------------
            # **********2.4GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 1 RX'):                    
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI2'
                return False
            RX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX2GHz\ChariotRX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX2GHz\ChariotRX2GHz.exe")
            self.i2GHzRXvalue = RX2GRESULT
            if RX2GRESULT < 100:
                self.Error_code = 'WF2RXV'                
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 1, None, RX2GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 1, None, RX2GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF2EX0'
            return False
        

    def _WiFi24GHz_6(self):
        #cmd = r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi24GHz6\WiFi24GHz6.exe"
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi24GHz6\WiFi24GHz6.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi24GHz6\WiFi24GHz6.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********2.4GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 6 TX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI1'
                return False
            TX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX2GHz\ChariotTX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX2GHz\ChariotTX2GHz.exe")
            self.i2GHzTXvalue = TX2GRESULT
            if TX2GRESULT < 100:
                self.Error_code = 'WF2TXV'                        
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 6, TX2GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 6, TX2GRESULT, None)
            # --------------------------------------------
            # **********2.4GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 6 RX'):
                    bcheckping = True
                    break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI2'
                return False
            RX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX2GHz\ChariotRX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX2GHz\ChariotRX2GHz.exe")
            self.i2GHzRXvalue = RX2GRESULT
            if RX2GRESULT < 100:
                self.Error_code = 'WF2RXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 6, None, RX2GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 6, None, RX2GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF2EX0'
            return False

    def _WiFi24GHz_11(self):
        #cmd = r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi24GHz11\WiFi24GHz11.exe"
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi24GHz11\WiFi24GHz11.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi24GHz11\WiFi24GHz11.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********2.4GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 11 TX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI1'
                return False
            TX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX2GHz\ChariotTX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX2GHz\ChariotTX2GHz.exe")
            self.i2GHzTXvalue = TX2GRESULT
            if TX2GRESULT < 100:
                self.Error_code = 'WF2TXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 11, TX2GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 11, TX2GRESULT, None)
            # --------------------------------------------
            # **********2.4GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF24GHzIP, 'Ping WiFi 2.4GHz Channel 11 RX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF2PI2'
                return False
            RX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX2GHz\ChariotRX2GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX2GHz\ChariotRX2GHz.exe")
            self.i2GHzRXvalue = RX2GRESULT
            if RX2GRESULT < 100:
                self.Error_code = 'WF2RXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 11, None, RX2GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 11, None, RX2GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF2EX0'
            return False

    def _WiFi5GHz_36(self):
        #cmd = r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetInfo\GetInfo.exe"
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi5GHz36\WiFi5GHz36.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi5GHz36\WiFi5GHz36.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********5GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 36 TX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI1'
                return False
            TX5GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX5GHz\ChariotTX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX5GHz\ChariotTX5GHz.exe")
            self.i5GHzTXvalue = TX5GRESULT
            if TX5GRESULT < 600:
                self.Error_code = 'WF5TXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 36, TX5GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 36, TX5GRESULT, None)
            # --------------------------------------------
            # **********5GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 36 RX'):
                    bcheckping = True
                    break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI2'
                return False
            RX5GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX5GHz\ChariotRX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX5GHz\ChariotRX5GHz.exe")
            self.i5GHzRXvalue = RX5GRESULT
            if RX5GRESULT < 600:
                self.Error_code = 'WF5RXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 36, None, RX5GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 36, None, RX5GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF5EX0'
            return False

    def _WiFi5GHz_48(self):
        #cmd = r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetInfo\GetInfo.exe"
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi5GHz48\WiFi5GHz48.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi5GHz48\WiFi5GHz48.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********5GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 48 TX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI1'
                return False
            TX5GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX5GHz\ChariotTX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX5GHz\ChariotTX5GHz.exe")
            self.i5GHzTXvalue = TX5GRESULT
            if TX5GRESULT < 600:
                self.Error_code = 'WF5TXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 48, TX5GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 48, TX5GRESULT, None)
            # --------------------------------------------
            # **********5GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 48 RX'):
                    bcheckping = True
                    break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI2'
                return False
            RX2GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX5GHz\ChariotRX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX5GHz\ChariotRX5GHz.exe")
            self.i5GHzRXvalue = RX5GRESULT
            if RX5GRESULT < 600:
                self.Error_code = 'WF5RXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 48, None, RX5GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 48, None, RX5GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF5EX0'
            return False

    def _WiFi5GHz_153(self):
        #cmd = r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\GetInfo\GetInfo.exe"
        try:
            cmd = r"D:\Test_Program\OBA_WIFI\WiFi5GHz36\WiFi5GHz153.exe" #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\VDTweb\dist\WiFi5GHz36\WiFi5GHz153.exe"
            print(cmd)
            buffer = ''
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, 'utf-8'):
                res = str(line, 'utf-8')
                buffer += res
                #print(res)
                self.log.insert(END,res)
                if not line: break
            p.stdout.close()
            p.wait()
            #self.fChariot.RunChariot()
            # --------------------------------------------
            # **********5GHz TX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            time.sleep(10)
            self._WiFi_Request(['connect', 'OBA-WiFi-2.4G'])
            Walive = 0
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 153 TX'):                   
                    Walive += 1
                    if Walive == 5:
                        bcheckping = True
                        break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI1'
                return False
            TX5GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotTX5GHz\ChariotTX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotTX5GHz\ChariotTX5GHz.exe")
            self.i5GHzTXvalue = TX5GRESULT
            if TX5GRESULT < 600:
                self.Error_code = 'WF5TXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 153, TX5GRESULT, None)
                return False        
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 153, TX5GRESULT, None)
            # --------------------------------------------
            # **********5GHz RX THROUGHPUT**********        
            # --------------------------------------------
            bcheckping = False
            for i in range(0, 40):
                if self.Check_Throughput_alive(1, self.WF5GHzIP, 'Ping WiFi 5GHz Channel 153 RX'):
                    bcheckping = True
                    break
                time.sleep(1)
            if not bcheckping:
                self.Error_code = 'WF5PI2'
                return False
            RX5GRESULT = self._Test_Throughput(r"D:\Test_Program\OBA_WIFI\ChariotRX5GHz\ChariotRX5GHz.exe") #r"D:\Manh\Source\Python\Module_Collection\oba\wifi\dist\ChariotRX5GHz\ChariotRX5GHz.exe")
            self.i5GHzRXvalue = RX5GRESULT
            if RX2GRESULT < 600:
                self.Error_code = 'WF5RXV'
                self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 153, None, RX5GRESULT)
                return False
            self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '5GHz', 153, None, RX5GRESULT)
            return True
        except Exception as e:
            print(e)
            self.Error_code = 'WF5EX0'
            return False

    def Self_test(self, a = 'a'):
            print('Self_test')
        #while self.Test_Flag:
            try:
                    self.iAllowTest = False
                #if not self.Test_Flag:                    
                    if self.bCheck_DUT_Alive:
                        print('Check DUT alive')
                        self.log.insert(END, 'Check DUT alive\r\n')
                        alive = 0
                        for i in range(0, 20):
                            if self.Check_DUT_alive():
                                alive += 1
                                if alive == 3:
                                    self.iAllowTest = True
                                    break
                            time.sleep(1)
                    if self.iAllowTest:                        
                        self.Update_Progress(10, itheme='default', istyle='green')
                        print('--------START CHECK WEB')                        
                        self.allowListen = True
                        self._Get_Setup()
                        self._Login_First()
                        self.Update_Progress(20, itheme='default', istyle='green')
                        if not self._Check_Info() :
                            self.Error_code = 'INFO01'
                            self.Test_Flag = False
                            self.Return_Result(False)
                            return False
                        print('***********')
                        print(self.DUTSN)
                        print('***********')
                        self.vDUTSN.set('SN: '+self.DUTSN)
                        self.Update_Progress(30, itheme='default', istyle='green')
                        self.bstart_test = True
                        self.iSerial.Send_COM(self.DUTSN + '\n')
                        if self.SFC_Comm_start(self.DUTSN):
                            self.bstart_test = False
                            self.bend_test = True
                            self.Update_Progress(40, itheme='default', istyle='green')
                            if self.Main_WiFi():                                
                                self.Test_Flag = False
                                self.Final_Result = True
                                self.Return_Result(True)
                                self.bend_test = False
                                self.allowListen = False
                                #self.Update_DataList('PASS', 'U46C420.00', self.DUTSN, '2.4GHz', 10)
                                return True
                                #breakpoint                                
                            else:
                                self.Test_Flag = False
                                #self.log.insert(END, 'Failed to check DUT alive\r\n')
                                #self.Error_code = 'EH00_01'
                                self.Return_Result(False)
                                self.bend_test = False
                                #self.Update_DataList('FAIL', 'U46C420.00', self.DUTSN, '2.4GHz', 10)
                                return False
                        else:
                            self.Test_Flag = False
                            #self.log.insert(END, 'Failed to check DUT alive\r\n')
                            #self.Error_code = 'EH00_01'
                            self.Return_Result(False)
                            self.bend_test = False
                            #self.Update_DataList('FAIL', 'U46C420.00', self.DUTSN, '2.4GHz', 10)
                            return False
                    else:
                        self.Test_Flag = False
                        self.log.insert(END, 'Failed to check DUT alive\r\n')
                        self.log.see(END)
                        self.Error_code = 'EH0001'
                        self.Return_Result(False)
                        self.bend_test = False
                        return False
                    self.bend_test = False
                    return False
                    #break
                    #time.sleep(0.2)
            except Exception as e:
                print('have a error occur')
                print(e)
                #time.sleep(1)

    def Return_Result(self,Fresult):
        print(Fresult)
        print('Error_code: ' + self.Error_code)
        self.Final_Result = False
        self.bend_test = True
        if Fresult:            
            self.iSerial.Send_COM(self.DUTSN + 'END\n')
            if self.SFC_Comm_end(self.DUTSN+'END'):
                self.Final_Result = True
            #print('pass')
            if self.Final_Result:
                self.lbStatus.configure(text='PASS', fg='white', bg='green')
                self.log.insert(END,'\r\n============================\r\nFinal Result:PASS\r\n============================\r\n')
                #monitor_data = ['end', socket.gethostname(), 'ONLINE', 'pass', '']
                self.cpass += 1
                self.Update_Progress(100, itheme='default', istyle='green')
                #self.PFStatus = 'PASS:' + str(self.cpass) + '   |   FAIL:' + str(self.cfail) + '    |   Created:' + self.CreateTime
                # self.Send_To_Monitor(monitor_data)
            else:
                self.lbStatus.configure(text='Fail: SFC_FAIL', fg='white', bg='red')
                self.log.insert(END,'\r\n============================\r\Result:SFC_FAIL1\r\n============================\r\n')
                self.log.insert(END,'\r\n============================\r\nFinal Result:FAIL\r\n============================\r\n')
                monitor_data = ['end', socket.gethostname(), 'ONLINE', 'fail', self.Error_code]
                self.cfail += 1
                self.Update_Progress(100, itheme='default', istyle='red')
                #self.PFStatus = 'PASS:' + str(self.cpass) + '   |   FAIL:' + str(self.cfail) + '    |   Created:' + self.CreateTime
                # self.Send_To_Monitor(monitor_data)
        else :
            self.Final_Result = False
            if self.Error_code != 'EH0001' and self.Error_code != 'INFO01':
                self.iSerial.Send_COM(self.DUTSN + 'END\n')
                if self.SFC_Comm_end(self.DUTSN+'END'):
                    self.lbStatus.configure(text='Fail: '+ self.Error_code, fg='white', bg='red')
                else:
                    self.lbStatus.configure(text='Fail: SFC_FAIL', fg='white', bg='red')
                    self.log.insert(END,'\r\n============================\r\Result:SFC_FAIL2\r\n============================\r\n')
            else:
                    self.lbStatus.configure(text='Fail: '+ self.Error_code, fg='white', bg='red')
            self.log.insert(END,'\r\n============================\r\nFinal Result:FAIL\r\n============================\r\n')
            #monitor_data = ['end', socket.gethostname(),'ONLINE', 'fail', self.Error_code]
            self.cfail += 1
            self.Update_Progress(100, itheme='default', istyle='red')
            #self.PFStatus = 'PASS:' + str(self.cpass) + '   |   FAIL:' + str(self.cfail) + '    |   Created:' + self.CreateTime
            #self.Send_To_Monitor(monitor_data)
        #self.lbLogTest.configure(text=self.PFStatus)
        self.log.see(END)
        self.End_Time = time.time()#datetime.now()        
        self._FPY_Func()
        self.bstart = False
        '''if self.Test_Type=='SCANNER':
            self.strscan.set('')
            self.Scan_Value.set('')
            self.txtScan_Value.configure(state='normal')
        if self.Test_Type=='SELF_NO_FIXTURE':
            self.btnStart.configure(state='disabled')
        # -------Test status------------------
        if path.isfile('D:/Test_program/Module/Main/data.json'):
            try:
                SFC_data_file = open('D:/Test_program/Module/Main/data.json', 'r')
                SFC_data = SFC_data_file.read().strip()
                SFC_data_file.close()
                data_value_list = literal_eval(SFC_data)
                data_value_list.update({'TEST_STATUS': 'COMPLETE'})
                data_value_list.update({'MACHINENAME': self.PC_Name})
                data_value_list.update({'TESTTIME': round(self.End_Time-self.Start_Time)})#(self.End_Time - self.Start_Time).seconds
                jdata_value_list = json.dumps(data_value_list)
                SFC_data_file = open('D:/Test_program/Module/Main/data.json', 'w')
                SFC_data_file.write(str(jdata_value_list))
                SFC_data_file.close()
            except:
                print('set test status fail')
        # -------Test status------------------
        if self.Module_Use_Fixture:
            print('open com')
            self.Open_COM()
        if str(self.Fixture_Open).upper() == 'AUTO': self.Send_COM('open\r\n')'''
        self.barCode = b''
        self.countTime = 0
        self.Test_Flag = False
        #self.SaveLog()
        #self.Backup_Data_Log()

        #self.Change_Ver_Info(self.Test_Control_Ver)
    
    def Test_Time(self):
        if self.countTime <= self.TimeOut and self.Test_Flag:
            self.countTime += 1
            self.lbTime.configure(text='Time: {}'.format(self.countTime))
            self.lbTime.after(1000, self.Test_Time)
        if self.countTime > self.TimeOut:
            #self.Return_Result(False)
            self.Test_Flag = False
            self.lbStatus.configure(text='Time Out', fg='white', bg='chocolate')
            self.countTime = 0
            self.Stop_Proc_OnFail()
            #-----------------------------------------------------
            '''if self.Test_Type == 'SCANNER':
                self.strscan.set('')
                self.Scan_Value.set('')
                self.txtScan_Value.configure(state='normal')
                self.btnStart.configure(state='normal')'''

    def GetContent(self,buf, strstart, strend):
        # strresult="none"
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult

    def SFC_Comm(self, iexpect=''):
        while self.bsfclive:
            if self.isfcOpen:                
                igetin = str(self.iSerial.Get_in(), 'utf-8')
                if igetin != '':
                    self.sfclog.insert(1.0, igetin + '\n')
                    print(igetin)
                    print(igetin.find(self.iSendSFC))
                    if igetin.find(self.iSendSFC) == 0:
                        if igetin == self.iSendSFC+'PASS':
                            if iexpect.upper()=='START' and self.bstart_test:
                                self.SFC_Comm_start(igetin)
                            elif iexpect.upper()=='END' and self.bend_test:
                                self.SFC_Comm_end(igetin)
                        elif igetin == self.iSendSFC+'ERRO':
                            if iexpect.upper()=='START' and self.bstart_test:
                                self.SFC_Comm_start(igetin)
                            elif iexpect.upper()=='END' and self.bend_test:
                                self.SFC_Comm_end(igetin)
                        else:
                            self.iSerial.Send_COM('IT FORMAT ERROR')
                time.sleep(0.2)
                
    def SFC_Comm_start(self, idata):
        #while self.bsfclive:
        for i in range(0, 20):
            if self.isfcOpen:                
                igetin = str(self.iSerial.Get_in(), 'utf-8')
                if igetin != '':
                    self.sfclog.insert(1.0, igetin + '\n')
                    print(igetin)
                    print(igetin.find(idata))
                    if igetin.find(idata) == 0:
                        if igetin == idata+'PASS':
                            if self.bstart_test:
                                return True
                                #self.SFCInfoOK = True
                                #self.iSerial.Send_COM('START RUN')
                        elif igetin.find('ERRO') > 0:
                            return False
                            #self.iSerial.Send_COM('STOP RUN')
                        else:
                            self.sfclog.insert(1.0, 'IT FORMAT ERROR\n')
                            return False
                            #self.iSerial.Send_COM('IT FORMAT ERROR')
            else:
                self.sfclog.insert(1.0, 'SFC COM not OPEN\n')
                return False
            time.sleep(1)
                
    def SFC_Comm_end(self, idata):
        for i in range(0, 20):
            if self.isfcOpen:                
                igetin = str(self.iSerial.Get_in(), 'utf-8')
                if igetin != '':
                    self.sfclog.insert(1.0, igetin + '\n')
                    print(igetin)
                    print(igetin.find(idata))
                    if igetin.find(idata) == 0:
                        if igetin == idata+'PASS':
                            if self.bend_test:
                                return True
                                #self.SFCInfoOK = True
                                #self.iSerial.Send_COM('START RUN')
                        elif igetin.find('ERRO') > 0:
                            return False
                            #self.iSerial.Send_COM('STOP RUN')
                        else:
                            self.sfclog.insert(1.0, 'IT FORMAT ERROR\n')
                            return False
                            #self.iSerial.Send_COM('IT FORMAT ERROR')
            else:
                self.sfclog.insert(1.0, 'SFC COM not OPEN\n')
                return False
            time.sleep(1)

    def _SFC_Control(self):
        Thread(target=self.SFC_Control).start()

    def SFC_Control(self):
        while self.bsfclive:
            # try:
            if self.isfcOpen:                
                igetin = str(self.iSerial.Get_in(), 'utf-8')
                if igetin != '':
                    self.sfclog.insert(1.0, igetin + '\n')
                    print(igetin)
                    print(igetin.find(self.iSendSFC))
                    if igetin.find(self.iSendSFC) == 0:
                        if igetin == self.iSendSFC+'PASS':
                            if self.bstart_test:
                                self.iSerial.Send_COM('START RUN')
                            elif self.bend_test:
                                self.iSerial.Send_COM('END RUN')
                        elif igetin == self.iSendSFC+'ERRO':
                            self.iSerial.Send_COM('STOP RUN')
                        else:
                            self.iSerial.Send_COM('IT FORMAT ERROR')
            time.sleep(0.2)


    def COM_Control(self):
        if self.btnOpenCOM['text'] == 'SFC_Closed':
            if self.iSerial.Open_COM(self.vconnected.get()):
                self.btnOpenCOM.configure(fg='white', bg='green', text='SFC_Opened')
                self.isfcOpen = True
                #self.iSendSFC = 'CP0123456789'
                #self.iSerial.Send_COM(self.iSendSFC)
            
        elif self.btnOpenCOM['text'] == 'SFC_Opened':            
            #self.iSendSFC = 'CP0123456789END'
            #self.iSerial.Send_COM(self.iSendSFC)
            if self.iSerial.Close_COM():
                self.btnOpenCOM.configure(fg='white', bg='red', text='SFC_Closed')
                self.isfcOpen = False

    def Open_COM(self):
        try:
            self.ser = serial.Serial(self.vconnected.get())
            print(self.ser.name)
            time.sleep(0.2)
            self.ser.flush()
            # self.ser.open()
            # self.ser.set_input_flow_control(enable=False)
            # self.ser.set_output_flow_control(enable=False)
            print('COM opened')
            self.btnOpenCOM.configure(fg='white', bg='green', text='SFC_Opened')
        except Exception as e:
            print(e)
            messagebox.showinfo('Open fail', 'Open COM fail')

    def Close_COM(self):
        try:
            self.ser.flush()
            time.sleep(0.2)
            self.ser.close()
            print('COM closed')
            self.btnOpenCOM.configure(fg='white', bg='red', text='SFC_Closed')
        except Exception as e:
            print(e)
        return True

    def Get_in(self):
        data_de = ''
        if not self.ser.is_open:
            print('re-open com')
            self.Open_COM()
        # time.sleep(0.1)
        # self.ser.flush()
        time.sleep(0.1)
        data_de = self.ser.read_all().strip()
        # time.sleep(0.1)
        self.ser.flush()
        if data_de != b'':
            print(self.ser.name)
            print('Fixture:' + str(data_de))
        return data_de

    def Send_COM(self, scmd):
        try:
            self.ser.write(scmd.encode())
            print('send to com ' + scmd + '\r\n')
            return True
        except Exception as e:
            print('send to com failed')
            print(e)
            messagebox.showinfo('Send SFC fail', 'Please open COM')
            return False

    def Check_DUT_alive(self, itime=1):
        print('Check DUT Alive')
        self.lbStatus.configure(text='Check DUT Alive', fg='white', bg='gold')
        self.log.insert(END, 'Check DUT Alive\r\n')
        self.log.see(END)
        cmd = "ping " + self.DUT_IP + " -n " + str(itime)
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
        p.stdout.close()
        p.wait()

        if buffer.find('Lost = 0 (0% loss)') > 0:
            try:
                sMIN = int(self.GetContent(buffer, 'Minimum = ', 'ms'))
                if sMIN < 8:
                    print('Check DUT alive pass')
                    return True
                else:
                    print('Check DUT alive fail')
                    return False
            except:
                print('Check DUT alive fail 1')
                return False
        else:
            print('Check DUT alive fail 2')
            return False

    def Check_Throughput_alive(self, itime=1, iIP='', itittle='Check Throughput Alive'):
        print(itittle)
        if iIP == '': return False
        self.lbStatus.configure(text=itittle, fg='white', bg='gold')
        self.log.insert(END, itittle+'\r\n')
        self.log.see(END)
        cmd = "ping " + iIP + " -n " + str(itime)
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            #print(res)
            self.log.insert(END,res)
            self.log.see(END)
            if not line: break
        p.stdout.close()
        p.wait()

        if buffer.find('Lost = 0 (0% loss)') > 0:
            try:
                sMIN = int(self.GetContent(buffer, 'Minimum = ', 'ms'))
                if sMIN < 15:
                    print('Check DUT alive pass')
                    return True
                else:
                    print('Check DUT alive fail')
                    return False
            except:
                print('Check DUT alive fail 1')
                return False
        else:
            print('Check DUT alive fail 2')
            return False

    def _WiFi_Request(self, iSendData):
        self.Open_SelfClient(iSendData)

    def Open_SelfServer(self):
        self.serversocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 65432
        self.serversocket.bind((host,port))

        self.serversocket.listen(5)
        connect=True
        while True:
            if self.allowListen:
                self.conn,self.client=self.serversocket.accept()
                try:
                        print('connection from: ',self.client)
                    #while self.conn:
                        infodata=self.conn.recv(1024).decode()
                        self.DUTSN = infodata
                        print('receive from client: ',infodata)
                        self.allowListen = False
                        '''a=Find_Password(data)
                        if a:
                           print('response to client: ',a)
                           conn.sendall(a.encode())
                        else:
                            print('no data')'''
                    
                except socket.error:
                   connect = False
                   '''self.serversocket=socket.socket()
                   print('wait connect...')
                   while not connect:
                      try:
                         self.serversocket.listen(5)
                         while True:
                            self.conn,self.client=self.serversocket.accept()
                      except socket.error:
                         time.sleep(1)'''

    def Open_SelfClient(self, iSendData):
        self.clientsocket = socket.socket()
        host='192.168.200.2'
        port = 65432
        self.clientsocket.connect((host,port))

        #self.clientsocket.listen(5)     
        while True:
            try:
                #infodata=self.conn.recv(1024).decode()
                #self.DUTSN = infodata
                #print('receive from server: ',infodata)
                #self.allowListen = False
                self.clientsocket.sendall(str(iSendData).encode())
                time.sleep(1)
                infodata=self.clientsocket.recv(1024).decode()
                print('receive from server: ',infodata)
                if infodata == 'OK':
                    break
                    
            except socket.error:
                connect = False
                   
    def Update_DataList(self, iresult, imodel, iSN, iWiFi, iChannel=None, iTX=None, iRX=None):
        idatetime = str(datetime.now().__format__('%d-%B-%Y'))+'    '+str(datetime.now().__format__('%H:%M:%S'))
        idata = (idatetime, iresult, imodel, iSN, iWiFi, iChannel, iTX, iRX)
        self.DataList.insert("", "0", values=(idata))

    def Change_theme(self, itheme, istyle):
        self.tStyle.theme_use('winnative')
        self.tStyle.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.tStyle.configure('green.Horizontal.TProgressbar', foreground='limegreen', background='limegreen')
        mstyle = istyle.lower() + '.Horizontal.TProgressbar'
        self.progress_bar.configure(style=mstyle)

    def Update_Progress(self, value, itheme, istyle):
        self.Change_theme(itheme, istyle)
        self.progress_bar['value'] = value
        self.progress_bar.update_idletasks()

    def Load_CFG(self):
        CFG_file = open('config.json', 'r')
        CFG_data = CFG_file.read().strip()
        CFG_file.close()
        self.cfg_value_list = literal_eval(CFG_data)
        self.DUT_IP = self.cfg_value_list['DUT_IP']
        self.WF24GHzIP = self.cfg_value_list['WiFi24GHz_IP']
        self.WF5GHzIP = self.cfg_value_list['WiFi5GHz_IP']
        self.WF6GHzIP = self.cfg_value_list['WiFi6GHz_IP']
        self.DUT_SN_Length = self.cfg_value_list['DUT_SN_Length']
        self.WiFi24GHz_SSID = self.cfg_value_list['WiFi24GHz_SSID']
        self.WiFi5GHz_SSID = self.cfg_value_list['WiFi5GHz_SSID']
        self.WiFi6GHz_SSID = self.cfg_value_list['WiFi6GHz_SSID']

    def Save_CFG(self):
        print('Save_CFG')

    def SaveLog(self):
        try:
            AllLog = self.log.get(1.0, END)
            datetosave = str(datetime.now().__format__('%d-%B-%Y'))
            timetosave = str(datetime.now().__format__('%d-%B-%Y_%H-%M-%S'))
            full_savedir = 'D:/Logs/' + self.Model + '/' + self.Station + '/' + self.PC_Name + '/' + datetosave
            savedir = 'Logs/'+self.Model + '/' + self.Station + '/' + self.PC_Name + '/' + datetosave
            if not os.path.isdir(full_savedir): os.makedirs(full_savedir)
            self.Get_Log_Name()
            if self.Test_Type == 'SELF':
                title_scan = 'Test Item  /  SN:' + self.Log_Result_Name
                self.lbListItem.configure(text=title_scan)
            if self.Test_Type == 'SELF_NO_FIXTURE':
                title_scan = 'Test Item  /  SN:' + self.Log_Result_Name
                self.lbListItem.configure(text=title_scan)
            log_file = open(full_savedir + '/' + self.Log_Result_Name + '_' + timetosave + '.txt', 'w')
            log_file.write(AllLog)
            log_file.close()
            if not path.isfile(full_savedir + '/Summary_Log.txt'):
                sum_file = open(full_savedir + '/Summary_Log.txt', 'w')
                Sum_File_Head = 'Result\tError_Code\tSN\tModel\tStation\tPC_Name\tMain_Version\tFinish_Date_Time\tTest_Time'
                sum_file.write(Sum_File_Head)
                sum_file.close()
                time.sleep(0.5)
            if self.Final_Result : total_result = 'PASS'
            else : total_result = 'FAIL'
            sum_file = open(full_savedir + '/Summary_Log.txt')
            sum_file.mode = 'r'
            sum_content = sum_file.read()
            sum_file.close()
            sum_file = open(full_savedir + '/Summary_Log.txt', 'w')
            sum_file.write(sum_content+'\n'+total_result+'\t'+self.Error_code+'\t'+self.Log_Result_Name+'\t'+self.Model+'\t'+self.Station+'\t'+str(self.PC_Name)+'\t'+self.Test_Control_Ver+
                           '\t'+timetosave+'\t'+str(round(self.End_Time - self.Start_Time)))#(self.End_Time - self.Start_Time).seconds
            sum_file.close()
            '''time.sleep(0.5)
            #if not path.isdir('D:/Test_program/Module/Main/Data_Logs'):os.makedirs('D:/Test_program/Module/Main/Data_Logs')
            #shutil.copy('D:/Test_program/Module/Main/data.json','D:/Test_program/Module/Main/'+self.Log_Result_Name+ '_' + timetosave + '.txt',savedir)
            for i in range(0,2):
                if path.isfile(full_savedir + '/' + self.Log_Result_Name+ '_' + timetosave + '.txt') and path.isfile(full_savedir + '/Summary_Log.txt'):
                    if not FTP_Trans.Upload_File(self.Log_IP, self.Log_User, self.Log_Password,
                                                 full_savedir + '/' + self.Log_Result_Name + '_' + timetosave + '.txt',savedir):
                        time.sleep(0.5)
                        if not FTP_Trans.Upload_File(self.Log_IP, self.Log_User, self.Log_Password,
                                                     full_savedir + '/' + self.Log_Result_Name + '_' + timetosave + '.txt',
                                                     savedir):
                            print('Save log to FTP fail')
                    if not FTP_Trans.Upload_File(self.Log_IP, self.Log_User, self.Log_Password,
                                                 full_savedir + '/Summary_Log.txt',savedir):
                        time.sleep(0.5)
                        if not FTP_Trans.Upload_File(self.Log_IP, self.Log_User, self.Log_Password,
                                                     full_savedir + '/Summary_Log.txt',savedir):
                            print('Save summary log to FTP fail')
                    break
                time.sleep(0.5)'''
        except Exception as e:
            print('save log fail')
            print(e)

    def _Kill_Process(self, KfuncName, itimeout):
        self.iKfuncName = KfuncName
        self.iKitimeout = itimeout
        Thread(target=self.Kill_Process).start()
    
    def Kill_Process(self):
        time.sleep(self.iKitimeout)
        print(os.system('taskkill /f /im '+self.iKfuncName))

    def Stop_Proc_OnFail(self):
        for proc in self.run_file_list:
            os.system('taskkill /f /im ' + proc)
            #print(os.system('taskkill /f /im ' + proc))
        for rproc in self.Process_Relate_list:
            os.system('taskkill /f /im ' + rproc)
    

def on_Closing():
    if messagebox.askokcancel('Exit Test Message', 'Bạn có chắc muốn thoát ?\n Are you sure you want to exit ?',
                              icon='warning'):
        #ftemp.cleanup()
        root.destroy()


root = Tk()
# root.geometry("400x200+200+200")
#root.attributes('-fullscreen',True)
root.state('zoomed')
root.protocol('WM_DELETE_WINDOW', on_Closing)
# root.iconbitmap('D:/Test_Program/Module/Main/icon.ico')
root.configure(background='lightskyblue')
app = App(master=root)
app.mainloop()

#if __name__=='__main__':
#    App_OBA_WiFi().Main_OBA_WiFi()
'''def Main_OBA_WiFi(self):        
        for i in range(0, 10):
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
                break
        for i in range(0, 30):
            i += 1
            print(i)
            time.sleep(1)
            if i == 9:                
                Thread(target=self.Login).start()
            elif i == 29:                
                Thread(target=self.WiFi24GHz).start()
        return True
                

    def Get_Setup(self):
        print('--------START Get_Setup')
        if self.first_Get_Setup == 0:
            #from VDTweb import Get_Setup
            xGet_Setup.LoadDUTlink()
            self.first_Get_Setup += 1
        else:
            xGet_Setup.LoadDUTlink()
            #importlib.reload(Get_Setup)
        #del Get_Setup

    def Login_First(self):
        from VDTweb import Login_First

    def Login(self):
        from VDTweb import Login

    def Check_Info(self):
        print('--------START GetInfo')
        if self.first_Check_Info == 0:
            self.first_Check_Info += 1
            #from VDTweb import GetInfo
            xGetInfo.LoadDUTlink()
        else:
            xGetInfo.LoadDUTlink()
            #importlib.reload(Get_Setup)
        #del GetInfo

    def WiFi24GHz(self):
        from VDTweb import WiFi24GHz

    def WiFi5GHz(self):
        from VDTweb import WiFi5GHz'''

    # ------------------------------------------------

'''
import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
'''

'''import json

with open('data.txt') as json_file:
    data = json.load(json_file)
    for p in data['people']:
        print('Name: ' + p['name'])
        print('Website: ' + p['website'])
        print('From: ' + p['from'])
        print('')'''
