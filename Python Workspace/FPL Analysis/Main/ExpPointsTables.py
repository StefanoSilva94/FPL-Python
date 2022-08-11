'''
Created on 3 Aug 2022

-Aim is to add expPts column to table and work it out by combining CS, Goal and Assist Points depending on position
-Need to decide is it easier to make eCSPts, eGoalpts, eAss Pts columns and then combine?
-Or make expPts from scratch (trying this first and then will try other method if too difficult/buggy)

@author: stefanosilva
'''
from Main import CreateDatabaseAndTables as cdt
import sqlite3




'''For each row works out the expected points of a player: 
    Def/GK = 4pt for CS, 6 for goal, 3 for Assist
    Mid = 1pt for CS, 5 for goal, 3 for Assist
    For = 0 for CS, 4 for goal, 3 for Assist
    Each player is assumed to score 2 points for starting and playing 60 mins
    No consideration for bonus points
'''

cdt.createeAss_CS_Goals_PriceTable()

def addExpPtsColToTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS expPts 
    AS SELECT * FROM eAss_CS_Goals_Price''')
    
    data=c.execute('''SELECT * FROM expPts''' )
    columns = data.description
    column = columns[8][0]
    
    if column == 'ePts':
        print("ePts col already exists in table")
        #column already exists in table 
    
    else:
        c.execute(''' ALTER TABLE expPts ADD ePts REAL END ''') 
    

    
    updateExpPointsForEachRow()

    conn.commit()
    conn.close()


def updateExpPointsForEachRow():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()

        
    c.execute('''UPDATE expPts
    SET ePts = 5
    WHERE Name = 'Salah' ''')
    
    conn.commit()
    conn.close()

    

        


def calculateExpPointsForRow(cs, goals, assist, pos):
    exPts = 2 #Assume 2 points for starting and playing 60 mins
    if pos == 'DEF' or pos == 'GKP':
        exPts = exPts + cs*4 + goals*6 + assist*3
    elif pos == 'MID':
        exPts = exPts + cs*1 + goals*5 + assist*3
    else:
        exPts = exPts + goals*4 + assist*3
        
    return str(exPts)

def createExpPtSingleGWTable(table, gw):
        conn =  sqlite3.connect('FPL_Predicted_Data.db')
        c = conn.cursor()
        
        c.execute('CREATE TABLE IF NOT EXISTS ' + table + gw + ''' (
        name TEXT,
        ePts REAL,
        price REAL,
        value REAL,
        GW TEXT 
        )''' )
        
        conn.commit()
        conn.close()


addExpPtsColToTable()
cdt.printTable('expPts', '3')





