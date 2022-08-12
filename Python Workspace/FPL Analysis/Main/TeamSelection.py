'''
Created on 5 Aug 2022
-This module is to pick the best team over the specified number of gameweeks
-*The aim is to recommend a list of potential transfers by working out the expPts 
for each player on your team and then comparing them to players at similar price points.
-*If two transfers are available than it will compare players in that position 
of the combined price of both players. d.g.:
If Robertson (Def, £7), Martinelli (Mid, £6) are the lowest exp scoring combo I want to find the
combination of a Def and Mid that will out score them for a price of £13
-Key functions:
i) getExpPtsOverMultGWs(startGW, endGW) is used to get a dataset of each players cumulative points over the specified gameweeks
that is sorted by Name alphabetically
ii) getMaxPlayerByColumn(data, column) to get the player with the most expected points/ppm that gameweek rangd. 
It also returns data with the row for the max player removed

@author: stefanosilva
'''

from Main import DataTransformation
from Main import ReadCSV
from Main import FPL_APIs
import math

f = FPL_APIs
d = DataTransformation
r = ReadCSV
m = math


# Locates the player with the highest player of the specified column (d.g.price or PPM or expPts) and then returns that player 
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



'''
Want to update this function:
-add another column to filter by position - return only players of that position
-sort final data by ppm and return max 50 rows
'''
def getExpPtsOverMultGWs(startGW, endGW):
    
    # d.g.: gw 1- gw5
    
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
        temp = d.addPPMToData(str(i))
        temp = temp[1]
        data = data + temp

    sumPts = []
    data = d.mergeSortArray(data)


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
    d.g. 
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
gw is the gameweek you want to make transfers for
numTransfers = number of transfers available
if numTransfers = 1, then it will look at the player with the lowest ppm and return all players 
that have a better ppm over the next 4 gameweeks at the players price or less and players position
if numTransfers = 2, then it will look at the 2 player with the lowest ppm and return all players 
that have a better ppm over the next 4 gameweeks at those players combine price in their positions

'''
def recommendTransfers(numTransfers, gw):
    transfer = []
    currentTeam  = findExpPtsAndPPMForCurrentSquad('3632826', str(gw - 1))[1:]
    # get data over 4 week range
    startGW = gw + 1; endGW = gw + 4
    data = getExpPtsOverMultGWs(startGW, endGW)
    if numTransfers == 1:
        for playerStats in currentTeam:
            print(playerStats[0])
            print(comparePlayer(playerStats, data))

    return transfer

'''
This will look at a player in my squads stats and compare to it players in data that are the same position 
and same price or less that will outscore the player
'''
def comparePlayer(player, data):
    cost = player[2]
    pos = player[3]
    expPts = player[4]
    posData = d.getDataByFilter(data, 'Position', pos)
    posAndCostData = d.getDataByFilter(posData, 'Cost', cost)
    # print(posAndCostData[1])    

    transfers = []
    
    for i in range(0,5):
        maxPlayer = getMaxPlayerByColumn(posAndCostData, 'expPts')[1]
        posAndCostData = getMaxPlayerByColumn(posAndCostData, 'expPts')[0]
        maxPlayerExpPts = maxPlayer[5]
    
        if maxPlayerExpPts > expPts:
            transfers.append(maxPlayer)
        else:
            # print(transfers)
            return transfers
        
 
    # print(transfers)
    return transfers

'''
Use data from 4 future gws. E.g.:
Assume most recent gameweek is input. 
If gw = 1, we want to find the expPts and PPM from gw2 - g4 (inclusive)
Add this for each player in current squad
Squad contains an array that holds the name and team of a player in the managers squad for the specified gameweek
Player represents each element of squad

'''
def findExpPtsAndPPMForCurrentSquad(managerId, gw):
    # Returns an array containing [name, team]
    squad = f.getManagerPlayers(managerId,gw)
    '''
    squad = [[Ward, LEI],...]
    '''
    squadStats = []
    expDataOverFourGWs = getExpPtsOverMultGWs(int(gw) + 1, int(gw) + 4)
    squadStats.append(['Name', 'Team', 'Cost', 'Position', 'ExpPts', 'PPM']) # Adding header
    
    playersFound = 0
    for row in expDataOverFourGWs[1]:
        if playersFound == 14: # If all players are found end the loop
            break
        else:
            name1 = row[1]
            team1 = row[2]
    
            for player in squad:
                name2 = player[0]
                team2 = player[1]
                if name1 == name2 and team1 == team2: # Check if player is in our squad
                    ''' 
                    player = [name, team]
                    row[3:] [Cost, Position, ExpPts, PPM]
                    player = [Name, Team, Cost, Position, ExpPts, PPM]
                    '''
                    player+=row[3:] 
                    squadStats.append(player) 
                    playersFound+=1
    return squadStats
    
recommendTransfers(1, 2)    
# player = ['Bailey', 'AVL', '5.0', 'MID', 14.9, 2.98]
# data = getExpPtsOverMultGWs(2, 5)
# comparePlayer(player, data)
# h = findExpPtsAndPPMForCurrentSquad('3632826', '1')
# print(h)
# a = getExpPtsOverMultGWs(1,5)
# b = d.getDataByFilter(a, 'Position', 'mid')
# r.printDataFromArray(h, 'rows')
# for i in range (0,20):
#     c = getMaxPlayerByColumn(b, 'ppm')
#     b = c[0]
#     player = c[1]
#     print(player)[[



