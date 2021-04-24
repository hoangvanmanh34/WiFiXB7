import time
import sys
import os
import re

from socket import *
from time import ctime







def client(ip):
     HOST='10.228.110.180'
     if '10.228.' in ip:
          HOST = '10.228.114.181'
     else:
          HOST = '10.228.110.180'
          
     PORT = 60001             
     ss = socket(AF_INET, SOCK_STREAM)
     ss.connect((HOST, PORT))
     #print(ss)
     #time.sleep(1.5)
     ss.send(ip.encode())
     print(ip.encode())
     ss.close() 

           
if __name__ == '__main__':      
    client('10.228.19.60')
    #client(sys.argv[1])

    
   
    

    
                
