'''
Created on 13 Aug 2022
@author: stefanosilva
'''
import csv
from Main import FPLReview as FPL
from Main import FPL_APIs

a = FPL.getAllProbabilityData()
csData = a[0]
gData = a[1]
aData = a[2]
minsData = FPL_APIs.getAllPlayersAvgMinutes()
'''
range of gws = startGW: startGW + 4 (GW3 -> GW7)
'''
def addCleanSheetDataToCSV():
    createCSVDataSheets("Cleansheet")
    
def addAssistDataToCSV():
    createCSVDataSheets("Assist")
    
def addGoalScorerDataToCSV():
    createCSVDataSheets("Goal")
    
def addAvgMinutesDataToCSV():
    createCSVDataSheets("Minutes")


def createCSVDataSheets(dataType):
    startGW = getStartGW()
    endGW = startGW + 5
    j = 0
    
    if dataType == 'Minutes':
        path = '/Users/stefanosilva/Documents/GitHub/FPL-Python/Python Workspace/FPL Analysis/Probability Data/'+ dataType + ' Data/CSV/minutes.csv'
        f = open(path, 'w')
        writer = csv.writer(f)
        writer.writerow(["Name","Team","avgMins"])
        for row in minsData:
            row = row[1:]
            writer.writerow(row)
        
    else:
        for i in range(startGW, endGW):
            path = '/Users/stefanosilva/Documents/GitHub/FPL-Python/Python Workspace/FPL Analysis/Probability Data/'+ dataType + ' Data/CSV/GW'
            path = path + str(i) + '.csv'
            f = open(path, 'w')
            writer = csv.writer(f)
            if dataType == "Cleansheet":
                rows = csData[j]
                writer.writerow(["Team","Opp","H/A","CS%"])
    
            elif dataType == "Assist":
                rows = aData[j]
                writer.writerow(["Name","Team","Fixture","eGoals/90","Anytime%"])
    
            else:
                rows = gData[j]
                writer.writerow(["Name","Team","Fixture","eAssists/90","Anytime%"])
            j+=1
            for row in rows:
                row = row[1:]
                writer.writerow(row)
        
        
    f.close()


def getStartGW():
    startGW = csData[0][1][0]
    splitGW = startGW.split("W")
    startGW = splitGW[-1]
    startGW = int(startGW)
    return startGW

addAvgMinutesDataToCSV()
addCleanSheetDataToCSV()
addAssistDataToCSV()
addGoalScorerDataToCSV()


