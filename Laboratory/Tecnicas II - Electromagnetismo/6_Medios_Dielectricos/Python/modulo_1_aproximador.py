# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:03:39 2023

@author: danie
"""


import numpy as np
from numpy.linalg import *
from matplotlib import *
from matplotlib import pyplot as plt
from IPython.display import display, Latex
import pandas as pd
import sympy as sy



def detectanueves(n,i):
    newn = ""
    while(n[i]=='9' and not(i<0)):
        n[i]==0
        i -= 1
        newn = "0"+newn
    if n[0]=="9":
        newn = "1"+ newn
    else:
        newn = "%d"%(int(n[0])+1) + newn
    return newn

def aproximaciondecimales(su):
    l = 0
    if su < 0.1:
        n = "{:.15f}".format(su)
        print(n)
        i = 0
        T = True
        while T:
            if(n[i]=="." or n[i]=="0"):
                if(n[i]=="."):
                    k = i
                i +=1
                print(i)
            else:
                T = False

        if (int(n[i+2])<5):
            aproxsu = "0."+"0"*(i-2) + "%d"%(int(n[i])) + "%d"%(int(n[i+1]))
    
        else: 
            y = "0."+"0"*(i-2)+"%s"%(n[i])+"%s"%(n[i+1]+"%d"%(5))
            x = float(y) 
            if (su - x > 0):
                if n[i+1]=="9":
                    l=detectanueves(n[i:i+2], 1)
                    if(n[i]!="9"):
                        aproxsu = "0."+"0"*(i-2)+l[0:2]
                    if(n[i]=="9"):
                        aproxsu = "0."+"0"*(i-3)+l[0:2]    
                else:
                    aproxsu = "0."+"0"*(i-2)+"%s"%(n[i])+"%d"%(int(n[i+1])+1)
            else:
                if ((int(n[i+1])%2) == 1):
                    if n[i+1]=="9":
                        l=detectanueves(n[i:i+2], 1)
                        if(n[i]!="9"):
                            aproxsu = "0."+"0"*(i-2)+l[0:2]
                        if(n[i]=="9"):
                            aproxsu = "0."+"0"*(i-3)+l[0:2]    
                    else:
                        aproxsu = "0."+"0"*(i-2)+"%s"%(n[i])+"%d"%(int(n[i+1])+1)
                else:
                    aproxsu = "0."+"0"*(i-2) + "%s"%(n[i]) + "%s"%(n[i+1])  
                    
                    
    if 0.1 < su  and su < 1:
        n = "{:.15f}".format(su)
        i = 2
        if (int(n[i+2])<5):
            aproxsu = "0."+"%s"%n[i] + "%s"%(n[i+1]) 
    
        else: 
            y = "0."+"%s"%n[i]+"%s"%(n[i+1])+"%d"%(5)
            x = float(y) 
            if (su - x > 0):
                if n[i+1]=="9":
                    l=detectanueves(n[i:i+2], 1)
                    if(n[i]!="9"):
                        aproxsu = "0."+l[0:2]
                    if(n[i]=="9"):
                        aproxsu = "1.0"   
                else:
                    aproxsu = "0."+"%s"%(n[i])+"%d"%(int(n[i+1])+1)
            else:
                if ((int(n[i+1])%2) == 1):
                    if n[i+1]=="9":
                        l=detectanueves(n[i:i+2], 1)
                        if(n[i]!="9"):
                            aproxsu = "0."+l[0:2]
                        if(n[i]=="9"):
                            aproxsu = "1.0"  
                    else:
                        aproxsu = "0."+"%s"%(n[i])+"%d"%(int(n[i+1])+1)
                else:
                    aproxsu = "0."+"0"*(i-2) + "%s"%(n[i]) + "%s"%(n[i+1])            
    if 1 < su and su < 10 :
        n = "{:.15f}".format(su)
        i = 0
        if (int(n[i+3])<5):
            aproxsu = "%s"%n[i] + "." + "%s"%(n[i+2]) 
    
        else: 
            y = "%s"%n[i] + "." + "%s"%(n[i+2])+"%d"%(5)
            x = float(y) 
            if (su - x > 0):
                if n[i+2]=="9":
                    l=detectanueves(n[i]+n[i+2], 1)
                    if(n[i]!="9"):
                        aproxsu = l[0]+"."+l[1]
                    if(n[i]=="9"):
                        aproxsu = "10"   
                else:
                    aproxsu = n[i]+"."+"%d"%(int(n[i+2])+1)
            else:
                if ((int(n[i+2])%2) == 1):
                    if n[i+1]=="9":
                        l=detectanueves(n[i]+n[i+2], 1)
                        if(n[i]!="9"):
                            aproxsu = l[0]+"."+l[1]
                        if(n[i]=="9"):
                            aproxsu = "10"   
                    else:
                        aproxsu = n[i]+"."+"%d"%(int(n[i+2])+1)
                else:
                    aproxsu = n[i]+"."+"%d"%(int(n[i+2]))
    if 10 < su:
        n = "{:.15f}".format(su)
        i = 0
        flag = True
        aproxsu=''
        if (int(n[2])<5):
            for j in range(len(n)):
                if n[j]=='.':
                    flag=False
                if flag and j<2:
                    aproxsu += "%s"%n[j] 
                if flag and j>=2:
                    aproxsu += "0"
        
        if (int(n[2])>5):
            for j in range(len(n)):
                if n[0]=="9" and n[1]=='9':
                    if n[j]=='.':
                        flag=False
                    if flag and j<2:
                        aproxsu = detectanueves(n[0:2], 1) 
                    if flag and j>=2:
                        aproxsu += "0"
                else:
                    if n[j]=='.':
                        flag=False
                    if flag and j==0:
                        aproxsu += "%s"%n[j] 
                    if flag and j==1:
                        aproxsu += "%s"%(int(n[j])+1)
                    if flag and j>=2:
                        aproxsu += "0"
                        
        if (int(n[2])==5):
            if(int(n[1])%2 == 0):
                for j in range(len(n)):
                    if n[j]=='.':
                        flag=False
                    if flag and j<2:
                        aproxsu += "%s"%n[j] 
                    if flag and j>=2:
                        aproxsu += "0"
                        
            if(int(n[1])%2 == 1):
                if n[0]=="9" and n[1]=='9':
                    for j in range(len(n)):
                        if n[j]=='.':
                            flag=False
                        if flag and j<2:
                            aproxsu = detectanueves(n[0:2], 1) 
                        if flag and j>=2:
                            aproxsu += "0"
                else:
                    for j in range(len(n)):
                        if n[j]=='.':
                            flag=False
                        if flag and j==0:
                            aproxsu += "%s"%n[j] 
                        if flag and j==1:
                            aproxsu += "%s"%(int(n[j])+1)
                        if flag and j>=2:
                            aproxsu += "0"   
                   
                        
                        
    if su == 0.1 or su == 1 or su == 10:
        if su == 0.1 or su == 1:
            aproxsu = "%.1f"%(su)
        if su == 10:
            aproxsu = "%d"%su
    
    aproxsu = float(aproxsu)
    return aproxsu

