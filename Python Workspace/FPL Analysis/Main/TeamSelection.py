'''
Created on 5 Aug 2022
-This module is to pick the best team over the specified number of gameweeks
-Then use 
-Key functions:
i) getExpPtsOverMultGWs(startGW, endGW) is used to get a dataset of each players cumulative points over the specified gameweeks
that is sorted by Name alphabetically
ii) getMaxPlayerByColumn(data, column) to get the player with the most expected points/ppm that gameweek range. 
It also returns data with the row for the max player removed
@author: stefanosilva
'''

from Main import ExpPoints
from Main import ReadCSV
from Main import FPL_APIs
import math


e = ExpPoints
r = ReadCSV
m = math

'''This is used to get all the player data in a 2d list for a specified gameweek
It contains extra columns that aren't needed in the final view,e.g.:
Fixture, eAss, eGoals, CS%, ...
'''
def pickTeam(gw):
    
    data = e.addPPMToData(gw)
    
    return data


# Locates the player with the highest player of the specified column (e.g.price or PPM or expPts) and then returns that player 
def getMaxPlayerByColumn(data, column):
    
    '''
    -rows = player data
    -m will contain the max column seen so far
    -rowNumber tracks the order of the max column in rows
    -maxRowNumber tracks how many rows have been looked at since the max was found
    -if a new max is located, we compute rowNumber = rowNumber + 1 + maxRowNumber to calculate 
    the current position of the max column. 
    '''
    
    if column.lower() == 'exppts':
        x = 5
    elif column.lower() == 'ppm' or column.lower() == 'value':
        x = 6
    else:
        print("You don't need to search the max value of that column")

    rows = data[1]
    m = 0 # m holds the highest expPts seen so far
    rowNumber = 0
    maxRowNumber = 0
    # iterate through each row, each row will be a unique player with their expPts in the 5th element of 'row'
    for row in rows:
        maxNew = row[x]
        if maxNew >= m:
            m = maxNew # m holds the highest expPts seen so far
            rowNumber = rowNumber + 1 + maxRowNumber
            maxRowNumber = 0
        else:
            maxRowNumber +=1 
    
    # -1 since arrays start at 0
    rowNumber -=1 
    
    player = rows[rowNumber]
    data[1].remove(player)

    return (data, player)


def getExpPtsOverMultGWs(startGW, endGW):
    
    # e.g.: gw 1- gw5
    
    ''' 
    -this should use  pickTeam(gw) for each gameweek and store them in an array
    -Sort alphabetically so that the players are all aligned
    -iterate through the array and sum the expPts
    -if two rows have the same name and team then it is the same player and you can add the expPts
    -if two rows DON'T have the same name and team then it is a new player
    '''
    data = []
    
    # Combining all gameweek data into one array and removing the header
    for i in range(startGW,endGW+1):
        temp = pickTeam(str(i))
        temp = temp[1]
        data = data + temp

    sumPts = []
    data = mergeSortArray(data)


    '''
    Takes gameweek data in alphabetical order
    If its the first time a name + team is seen add:
    gwks: number of gameweeks
    name
    team
    cost
    position
    expPts
    ppM: Total expPts / price
    to an array called row
    e.g. 
    James, CHE
    James,CHE
        
    If the name + team has already been seen then it is the next gameweek for the player
    Add the expPts to row[5] to get the cumulative points over multiple gameweeks     
    '''
    i = 0;
    oldName = 'placeholder'
    oldTeam = 'placeholder'
    gwks = endGW + 1 - startGW
        
    while i < len(data):
        name = data[i][1]
        team = data[i][2]
        

        if oldName != name or oldTeam != team:
            cost = data[i][7]
            position = data[i][8]
            expPts = data[i][9]
            
            row = [gwks, name, team, cost, position, expPts]
            value = row[5]/float(row[3])
            row.append(value)
            
            oldName = name
            oldTeam = team
            sumPts.append(row)

            i+=1
        
            '''
            If the name + team has already been seen then it is the next gameweek for the player
            Add the expPts to row[5] to get the cumulative points over multiple gameweeks
            '''  
        else:
            row[5] = row[5] + data[i][9] #Add expPts
            row[6] = row[5]/float(row[3])
            i+=1
            
    out = []
    
    header = ['GWKS', 'Name', 'Team', 'Cost', 'Position', 'expPts', 'PPM']
    
    out.append(header)
    out.append(sumPts)
    
    return out
 
 
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


a = getExpPtsOverMultGWs(2,5)
# a = pickTeam('2')
# a = a[1]
# b = mergeSortArray(a)



# for i in range(0,100):
#     b = getMaxPlayerByColumn(a,'exppts')
#     print(b)
#     c = []
#     d = []
#     c = a[1].remove(b)
#     d.append(a[0])
#     d.append(a[1])
#     a = d
    
for i in range (0,10):
    b = getMaxPlayerByColumn(a, 'exppts')
    a = b[0]
    player = b[1]
    print(player)


