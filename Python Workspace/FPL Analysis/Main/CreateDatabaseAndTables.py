'''
Created on 3 Aug 2022 

-This module is used to create the initial tables using data that is stored locally on CSV files
-All derived columns and transformations are on the ExpPointsTables Page
-Before running these functions make sure that the latest Player Price, exp Goals, expAss and exp CS 
data is saved in their respective folder in FPL Analysis folder
e.g. FPL Analysis/Goal Data/CSV/GWX (X Denotes gameweek number)
-Final Table that is needed is eAss_CS_Goal_Price that contains all the relevant data in one table
-PrintTable function is used to visualise the tables

@author: stefanosilva
'''
import sqlite3
from Main import ReadCSV



def dropTable(table):
    conn =  sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    c.execute('DROP TABLE ' + table)
    
    conn.commit()
    conn.close()

def createDatabase():
    conn =  sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT  EXISTS Cleansheet_Data (
    Team TEXT,
    Opp TEXT,
    HorA TEXT,
    CS REAL,
    GW TEXT)''' )
    
    
    conn.commit()
    conn.close()

def checkCols(table):
    
    conn =  sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    data=c.execute('''SELECT * FROM ''' + table)
    for column in data.description:
        print(column[0])
    conn.commit()
    conn.close()
    
    
'''checks if gw data is in table, adds if missing'''
def addCleanSheetRowsToTable(gw):
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    
    loadDataForMissingGameWeeks(gw, 'Cleansheet', 'Cleansheet_Data', conn)
        

    conn.commit()
    conn.close()
    
'''Checks if the data for the specified gameweek has been loaded - if not that data is loaded. 
This is to avoid data duplication when loading new gameweeks'''
def loadDataForMissingGameWeeks(gw, data, table, conn):
    c = conn.cursor()
    for x in range(1, gw+1):
        x = str(x)
        rows =  ReadCSV.getProbabilityData(data,x)[1]
        
        c.execute('SELECT * FROM ' + table + ' WHERE GW ='+x+' LIMIT 5')
        result = c.fetchone()
        
        if result == None:
            for row in rows:
                c.execute('INSERT INTO ' + table + ' VALUES (?,?,?,?,?)',row)
        
        else:
                print("Gameweek " + x + " data already added to table")
    


def createAssistTable():
    conn =  sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT  EXISTS Assist_Data (
    Name TEXT,
    Team TEXT,
    Fixture TEXT,
    eAss REAL,
    GW TEXT)''' )

    conn.commit()
    conn.close() 
     
    
'''checks if gw data is in table, adds if missing'''
def addAssistRowsToTable(gw):
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    
    loadDataForMissingGameWeeks(gw, 'Assist', 'Assist_Data', conn)
        

    conn.commit()
    conn.close()
    

def createGoalsTable():
    conn =  sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT  EXISTS Goal_Data (
    Name TEXT,
    Team TEXT,
    Fixture TEXT,
    eGoals REAL,
    GW TEXT)''' )

    conn.commit()
    conn.close()
    
 
def addGoalRowsToTable(gw):
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    
    loadDataForMissingGameWeeks(gw, 'Goal', 'Goal_Data', conn)
        
    conn.commit()
    conn.close()  
    
    
def createPriceTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS Player_Prices (
    Name TEXT,
    Team TEXT,
    Position TEXT,
    Price REAL
    )''' )

    conn.commit()
    conn.close() 
    
def addPriceRowsToTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    rows = ReadCSV.getProbabilityData('Price', 'Player Prices')[1]
    for row in rows:
        c.execute('INSERT INTO Player_Prices VALUES (?,?,?,?)',row)
        

    
    conn.commit()
    conn.close()


def printTable(table, rowsReturned):
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM ''' + table)
    headers = [i[0] for i in c.description]
    print(headers)
    
    c.execute('SELECT * FROM ' + table + ' LIMIT '+ rowsReturned)
    result = c.fetchall()
    
    for row in result:
        print(row)
    print("\n")
    conn.commit()
    conn.close()
    
'''joins assist table and CS table together as eAss_CS'''
def createeAss_CSTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS eAss_CS 
    AS SELECT a.Name, a.Team, c.CS, a.eAss, a.GW FROM Assist_Data as a
    INNER JOIN Cleansheet_Data as c
    ON a.Team = c.Team
    WHERE a.gw = c.gw''')
    
    conn.commit()
    conn.close()
    
 
'''joins assist table, CS table AND Goal table together as eAss_CS_Goal'''   
def createeAss_CS_GoalsTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS eAss_CS_Goals 
    AS SELECT a.Name, a.Team, a.CS, b.eGoals, a.eAss, a.GW FROM eAss_CS as a
    INNER JOIN Goal_Data as b
    ON a.Name = b.Name
    WHERE a.gw = b.gw''')
    
    conn.commit()
    conn.close()
    
    
'''joins assist table, CS table, Goal And Price table together as eAss_CS_Goal_Price'''     
def createeAss_CS_Goals_PriceTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS eAss_CS_Goals_Price 
    AS SELECT a.Name, a.Team, b.Position, b.Price, a.CS, a.eGoals, a.eAss, a.GW FROM eAss_CS_Goals as a
    INNER JOIN Player_Prices as b
    ON a.Name = b.Name
    ''')
    
    conn.commit()
    conn.close()
    

'''change query to run whatever is needed'''   
def runQuery():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    

    c.execute('SELECT * FROM eAss_CS  WHERE rowid = 50 LIMIT 2')
    
    result = c.fetchall()
    for row in result:
        print(row)
    conn.close()


def updateTable():
    conn = sqlite3.connect('FPL_Predicted_Data.db')
    c = conn.cursor()
    
    c.execute("UPDATE  eAss_CS_Goals_Price SET Price = Price + 1")
    
    conn.commit()
    conn.close()
    
    

'''Need all cols in one table:
-SELECT Name, Team, CS, eAss, eGoals, Position, Price 
-Need to add CS data to eAss table, then add egGoals, then add Price and Position
-Then can add derived columns:exPts, value etc 
'''
    
    
    

'''Creating  Clean Sheet Table'''             
dropTable('Cleansheet_Data')    
createDatabase()
addCleanSheetRowsToTable(5)
'''Creating  Assist Table''' 
dropTable('Assist_Data')
createAssistTable()
addAssistRowsToTable(5)
'''Creating  Goal Table''' 
dropTable('Goal_Data')
createGoalsTable()
addGoalRowsToTable(5)
dropTable('Player_Prices')
createPriceTable()
addPriceRowsToTable()
dropTable('eAss_CS')
createeAss_CSTable()
dropTable('eAss_CS_Goals')
createeAss_CS_GoalsTable()
dropTable('eAss_CS_Goals_Price')
createeAss_CS_Goals_PriceTable()



# printTable('eAss_CS', '6')
# printTable('eAss_CS_Goals', '6')
updateTable()
printTable('eAss_CS_Goals_Price', '3')

# printTable("Cleansheet_Data", "3")
# printTable("Assist_Data", "3")
# printTable("Goal_Data", "3")
# printTable("Player_Prices", "3")
# runQuery()




'''next tasks:
1)
- work out each players expected points for gameweek
- store in GWXExpPts table

2)
-create table for each players expected points over the next 5 gws

3)
-create algorithm to select players on best value
-optimise team by comparing value of players


'''




