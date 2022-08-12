'''
Created on 5 Aug 2022
This module takes an array containing assist, goal and cleansheet odds for each gameweek and 
calculates the expPoints for each player that week
Any functions that manipulate/transform the data within arrays are stored here
Any functions that output data directly useful for the end user are stored in team selection
@author: stefanosilva
'''
from Main import ReadCSV
import math

r = ReadCSV
m = math

'''
def/gk = 4*CS
mid = CS
for = 0

'''
'''This is used to get all the player data in a 2d list for a specified gameweek
It contains extra columns that aren't needed in the final view,d.g.:
Fixture, eAss, eGoals, CS%, ...
'''
def pickTeam(gw):
    
    data = addPPMToData(gw)
    
    return data

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

 
'''
This sorts the data by name alphabetically, if two names are the same it should consider the 
team as well. The other columns in the row will need to be moved in the same order as the name.
It is an adapted merge sort algorithm 
NOTE: l = 3 clause might be redundant but was useful in helping to visualise the logic of the merge sort
'''   

def mergeSortArray(data):
    '''
    needs to have no header row
    takes an array of arrays, last value is price, sort by price
    r1 = [1,'Adams', 'TOT', '(H): SOU', '0.33', '0.28', 0.44, '4.0', 'DEF','6.43']
    r2 = [1, 'Adams', 'BOU', '(H): LIV', '0.33', '0.28', 0.44, '4.0', 'DEF','8.47']
    data = (r1,r2)
    
    a= r1, b= r2
    
    if data = (r1,r2,r3):
    split data into data1 = (r1,r2)
    
    '''
    out = []

    # length of a and b should be the same
    l = len(data) 
    
    '''
    sorting 2 arrays alphabetically by name, if names are the same check team
    a[1] = name, b[1] = name
    a[2] = team, b[2] = team
    '''
    if l == 2:
        a = data[0]
        b = data[1]
        if a[1] < b[1]:
            out.append(a)
            out.append(b)
        elif a[1] > b[1]:
            out.append(b)
            out.append(a)
        else:
            if a[2] < b[2]:
                out.append(a)
                out.append(b)
            else:
                out.append(b)
                out.append(a)
                
    elif l == 3:

        r1 = data[:2]  
        r2 = data[2]
        r3 = mergeSortArray(r1)  
        
        out = mergeSortedArrays(r3, r2)
    
    else:
        ''' 
        [r1,r2,r3,r4,r5] --> a = [r1,r2] b = [r1,r2,r3]
        c = mergeSort(a) d = mergeSort(b)
        out = mergeSortedArray(c,d)
        '''
        mid = m.floor(l/2)
        a = data[:mid]
        b = data[mid:]
        c = mergeSortArray(a)
        d = mergeSortArray(b)
        
        out = mergeSortedArrays(c, d)
    return out
        

def mergeSortedArrays(a,b):
    '''
    This takes two already sorted arrays, merges them into tone sorted array
    
    r1 = [1,'Adams', 'TOT', '(H): SOU', '0.33', '0.28', 0.44, '4.0', 'DEF','6.43']
    r2 = [1,'Kane', 'TOT', '(H): SOU', '0.33', '0.28', 0.44, '4.0', 'DEF','6.43']
    r3 = [1, 'Adams', 'BOU', '(H): LIV', '0.33', '0.28', 0.44, '4.0', 'DEF','8.47']
    
    a = (r1,r2), b = r3
    out = (r3,r1,r2)
    
        
    '''
    out = []
    i = j = 0
    if countList(a) == 0 and countList(b) == 0:
        if a[1] < b[1]:
            out.append(a)
            out.append(b)
        elif b[1] < a[1]:
            out.append(b)
            out.append(a)
        else:
            if a[2] < b[2]:
                out.append(a)
                out.append(b)
            else:
                out.append(b)
                out.append(a)
    
    elif countList(b) == 0:

        while i < len(a) and j < 1:

            if a[i][1] < b[1]:

                out.append(a[i])
                i+=1
            elif a[i][1] > b[1]:
                out.append(b)
                j+=1
            else:
                if a[i][2]  < b[2]:
                    out.append(a[i])
                    i+=1  
                else:
                    out.append(b)
                    j+=1
              
        if i < len(a):
            for i in range(i,len(a)):
                out.append(a[i])

                       
        if j < 1:
            out.append(b)
                    
        
                    
    elif countList(a) == 0:

        while i < 1 and j < len(b):     

            if a[1] < b[i][1]:
                out.append(a)
                i+=1
            elif a[1] > b[i][1]:
                out.append(b)
                j+=1
            else:
                if a[2]  < b[i][2]:
                    out.append(a)
                    i+=1  
                else:
                    out.append(b[i])
                    j+=1  
                    
        if i < 1:
            out.append(a)
                     
        if j < len(b):
            for k in range(j,len(b)):
                out.append(b[k])                  
                    
    else:

        while i < len(a) and j < len(b):     
        
            if a[i][1] < b[j][1]:
                out.append(a[i])
                i+=1
            elif a[i][1] > b[j][1]:
                out.append(b[j])
                j+=1
            else:
                if a[i][2]  < b[j][2]:
                    out.append(a[i])
                    i+=1  
                else:
                    out.append(b[j])
                    j+=1
        
    
        if i < len(a):
            for i in range(i,len(a)):
                out.append(a[i])
            
            
        if j < len(b):
            for j in range(j,len(b)):
                out.append(b[j])
         
    return out

        


'''
countList is used because len(List) was not useful when counting 1D Lists
e.g.
len [1,2,3,4] -> 4 (but desired answer is 1)
len [[1,2,3,4],[5,6,7,8]] -> 2
'''
def countList(lst):
    count = 0
    for el in lst:
        if type(el)== type([]):
            count+= 1         
    return count

'''
this function looks at the header column of data and if your filter is present it will return only rows matching that value
If filt = price it will only return players of that price or lower
E.g.:
filter on Position, wwith value = DEF
'''
def getDataByFilter(data, filt, value):
    
    header = data[0]
    rows = data[1]
    newRows = []
    newRows.append(header)
    newRows.append([])
    
    count = 0
    # locate the postion of the filt col
    for column in header:
        if column.lower() != filt.lower():
            count+=1
        else:
            break
        
    if filt.lower() == 'price' or filt.lower() == 'cost':
        
        for row in rows:
            if float(row[count]) <= float(value):

                newRows[1].append(row)
    else:
        # if the value in row matches the input value add that row to newRow  
        for row in rows:
            if row[count].lower() == value.lower():
                newRows[1].append(row)
            
  
    return newRows
    
    


# a = addPPMToData('1')
# b = getDataByFilter(a,'position','Mid')
# b = getDataByFilter(b,'Cost','5.0')
# r.printDataFromArray(b, 'header')
# r.printDataFromArray(b, 'rows')


        
        