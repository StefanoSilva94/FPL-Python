'''
Created on 5 Aug 2022
This module takes an array containing assist, goal and cleansheet odds for each gameweek and 
calculates the expPoints for each player that week
@author: stefanosilva
'''
import ReadCSV
r = ReadCSV


'''
def/gk = 4*CS
mid = CS
for = 0

'''


def addExpPtsToData(gw):
    
    data = getGameweekData(gw)
    data[0].append("expPts")
    
    rows = data[1]
    
    for row in rows:
        a = row[4]
        g = row[5]
        cs = row[6]
        pos = row[8]
     
        expPts = cleanSheetPts(pos,cs) + assistPts(a) + goalPts(pos,g) + 2
        row.append(expPts)

    return data




# Points per million added for each player
def addPPMToData(gw):
    
    data = addExpPtsToData(gw)
    data[0].append("PPM")
    rows = data[1]
    
    for row in rows:
        expPts = float(row[9])
        price = float(row[7])
        ppm = expPts/price
        row.append(ppm)

    return data
    

def getGameweekData(gw):
    cs = r.getProbabilityData('Cleansheet', gw)
    a = r.getProbabilityData('Assist', gw)
    g = r.getProbabilityData('Goal', gw)
    p = r.getProbabilityData('Price', gw)
    
    data = r.mergePriceToCSAssistAndGoalData(a, g, cs, p)
    
    return data


def cleanSheetPts(pos, cs):
    
    if pos == 'DEF' or pos == 'GKP':
        exCSPts = 4 * cs
    elif pos == 'MID':
        exCSPts = cs
    else:
        exCSPts = 0;
        
    return float(exCSPts)

# 3 points for an assist for all positions
def assistPts(eAssist):
    eAssist = float(eAssist)
    exAPts =  3 * eAssist
    
    return exAPts

# goal points: 6 ptsfor def/gkp, 5 for mid, 4 for for 
def goalPts(pos, eGoals):
    
    eGoals = float(eGoals)
    
    if pos == 'DEF' or pos == 'GKP':
        exGPts = 6 * eGoals
    elif pos == 'MID':
        exGPts = 5 * eGoals
    else:
        exGPts = 4 * eGoals
        
    return exGPts


# a = addExpPtsToData('1')
# r.printDataFromArray(a, 'header')
# r.printDataFromArray(a, 'rows')


        
        