'''
Created on 9 Aug 2022

@author: stefanosilva
'''
import sqlite3
import TeamSelection
t = TeamSelection

def createDB():
    conn = sqlite3.connect("FPL_DB")
    c = conn.cursor()
    conn.close()
    



