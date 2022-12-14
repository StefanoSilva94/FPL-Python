'''
Created on 2 Aug 2022
The purpose of this page is to create functions that will combine 
price, CS, goals, assist and gw data into one array
@author: stefanosilva
'''
import csv
import os

'''This will read the data from a csv and return two values:
header - an array containg the header values
rows - 2d array, each subarray contains the non empty data on a row'''
def getDataFromCSV(filepath):
    cS1File = open(filepath)
    type(cS1File)
    csvreader = csv.reader(cS1File)

    '''next() method returns the current row and moves to the next row '''
    header = next(csvreader)
    '''remove unwanted rows'''
    header = header[0:4]
    
    '''rows is an array of arrays - each sub array contains a row of the csv'''
    rows = []
    for row in csvreader:
        rows.append(row[0:4])
        
    return header, rows


teamNames = {
  "Liverpool": "LIV",
  "Spurs": "TOT",
  "Newcastle": 'NEW',
  'Man City': 'MCI',
  'Chelsea': 'CHE',
  "Leicester": "LEI",
  "Man Utd": "MUN",
  "Aston Villa": 'AVL',
  'Leeds': 'LEE',
  'Arsenal': 'ARS',
  'Bournemouth': 'BOU',
  'Wolves': 'WOL',
  'Crystal Palace': 'CRY',
  'Brighton': 'BHA',
  'Brentford': 'BRE',
  'Everton': 'EVE',
  "Nott'm Forest": 'NFO',
  'West Ham': 'WHU',
  'Southampton': 'SOU',
  'Fulham': 'FUL',
}
  
  

def printDataFromArray(arr, section):
    if section == 'header':
        print(arr[0])
    else:
        for row in arr[1]:
            print(row)
        
    
'''returns a 2darray, first array contains the header, second is 2d array contain CS rows'''

def getProbabilityData(data, gw):
    # cwd = os.getcwd()  # Get the current working directory (cwd)
    # files = os.listdir(cwd)  # Get all the files in that directory
    # print("Files in %r: %s" % (cwd, files))

    path = '/Users/stefanosilva/Documents/GitHub/FPL-Python/Python Workspace/FPL Analysis/'
    os.chdir(path)
    if data == "Cleansheet":
        newData = getDataFromCSV('Probability Data/'+data+' Data/CSV/GW'+gw+'.csv')
        newData = updateCleanSheetOddsFromPercentToDec(newData)
        newData = changeTeamNameToAbbreviation(newData)
        newData = addGameweekToArray(newData, gw)
    elif data == 'Price':
        newData = getDataFromCSV('Probability Data/'+data+' Data/CSV/Player Prices.csv')
    elif data == 'Minutes':
        newData = getDataFromCSV('Probability Data/'+data+' Data/CSV/minutes.csv')
        
    else:
        newData = getDataFromCSV('Probability Data/'+data+' Data/CSV/GW'+gw+'.csv')
        newData = addGameweekToArray(newData, gw)
    
    return newData

        


def convertPercentToDecimal(percentage):
    '''This removes the last character '%', casts the number to a decimal (float)'''
    decimal = percentage[:-1]
    decimal = float(decimal)/100

    return decimal


'''takes 2d array, takes the percentage value in each subarray and converts to decimal'''
def updateCleanSheetOddsFromPercentToDec(array):
    for row in array[1]:
        row[3] = convertPercentToDecimal(row[3])
        
    return array


'''returns a 2darray, first array contains the header, second is 2d array contain Assist rows'''  
def getAssistData(gw):
    assistData = getDataFromCSV('Assist Data/CSV/GW'+gw+'.csv')
    assistData = addGameweekToArray(assistData, gw)
    return assistData    


'''returns a 2darray, first array contains the header, second is 2d array contain GS rows'''  
def getGoalScorerData(gw):
    goalScorerData = getDataFromCSV('Goal Data/CSV/GW'+gw+'.csv')
    goalScorerData = addGameweekToArray(goalScorerData, gw)
    return goalScorerData 

'''Update team names to abreviations so that they have a consistent value across different tables'''
def changeTeamNameToAbbreviation(csData):
    for row in csData[1]:
        row[0] = teamNames[row[0]]

    return csData

'''takes 2d array as input, header as first array, second array is sub array with data in each row
for either CS, GS, or Ass. It appends gameeek to each row'''
def addGameweekToArray(array, gw):
    gw = int(gw)
    array[0].insert(0,'GW')
    for row in array[1]:
        row = row.insert(0,gw)
    return array
    
    
'''
2d arrays: 1st array contain header columns, 2nd
Assist = Name, Team, Fixture, eAssists 
Goal = Name, Team, Fixture, eGoals
AssistAndGoals = Name, Team, Fixture, eAssists, eGoals
'''
def mergeAssistAndGoalData(aArray, gArray):
    '''convert all data into 2d array '''
    assistAndGoal = []
    
    # add header
    assistAndGoal.append(aArray[0])
    assistAndGoal.append(aArray[1])
    assistAndGoal[0].append(gArray[0][4])
    
    
    for i in range(0, len(assistAndGoal[1])):
        name = assistAndGoal[1][i][1]
        goals = getGoalOddsForPlayer(gArray, name)
        assistAndGoal[1][i].append(goals)

    
    return assistAndGoal


def mergeCleanSheetToAssistAndGoalData(aArray, gArray, csArray):
    
    csAssistGoal = mergeAssistAndGoalData(aArray, gArray)
    
    # Adding CS  to the header
    csAssistGoal[0].append(csArray[0][4])

    for i in range (0, len(csAssistGoal[1])):
        # get team name from assist and goal table
        team = csAssistGoal[1][i][2]
        # Find the cleansheet odds for that team
        csOdds = getCSOddsForTeam(csArray,team)
        csAssistGoal[1][i].append(csOdds)
    
    
    return csAssistGoal

# This adds the price, position and minutes for each player to the assist, goals and cleansheet array
def mergePriceAndMinutesToCSAssistAndGoalData(aArray, gArray, csArray, pArray, mArray):
    
    data = mergeCleanSheetToAssistAndGoalData(aArray, gArray, csArray)
    
    # Add price and pos to and header
    data[0].append(pArray[0][3])
    data[0].append(pArray[0][2])
    data[0].append("AvgMins")
    
    l = len(data[1])
    
    for i in range (0, l):
        # print(i)
        # get team name from assist and goal table
        name = data[1][i][1]
        team = data[1][i][2]
        
        # Find the cleansheet odds for that team
        price = getPlayerPositionAndPriceFromName(pArray,name,team)[0]
        pos = getPlayerPositionAndPriceFromName(pArray,name,team)[1]
        avgMins = getPlayerAvgMinutesFromName(mArray, name, team)

        data[1][i].append(price)   
        data[1][i].append(pos) 
        data[1][i].append(avgMins)
        
    return data

# This takes a team and looks for the corresponding cleansheet odds for that team in  CSdata    
def getCSOddsForTeam(csData, team1):
    rows = csData[1]
    team2 = ''

    i = 0
    while team1 != team2 and i < len(csData[1]):
        # Assign team2 = team in the ith row
        team2 = rows[i][1] 
        i+=1
 
    if team1 == team2:    
        csOdss = rows[i-1][4]
    else:
        return 999
    
    
    return csOdss


def getGoalOddsForPlayer(gData, name1):
    rows = gData[1]
    name2 = ''
    
    
    i = 0
    while name1 != name2 and i < len(gData[1]):
        # Assign name2 = name in the ith row
        name2 = rows[i][1] 
        i+=1 
    
    if name1 == name2:  
        goals = rows[i-1][4]

    else:

        print("couldn't find name on list")
        goals = 0

    
    return goals

'''
This function has been edited to accomadte special cases where names have been spelt differently across spreadsheets:
All EXCEPT BRYAN GIL are referred to by their second name
name1 -> name2
Ashley Young -> Young
Cody Drameh -> Drameh
R??ben Vinagre -> Vinagre
Daniel Iversen -> Iversen
Bryan Gil -> Bryan
All other players are like for like name1 = name2
Special elif clause for Bryan Gil, othere special cases use split(" ") to get their last name
'''
def getPlayerPositionAndPriceFromName(priceData, name1, team1):
    rows = priceData[1]
    name2 = ''
    team2 = ''
    names = name1.split(" ")
    lastName = names[-1]

    i = 0
    while i < len(priceData[1]):
        # Assign name2 = name in the ith row
        
        name2 = rows[i][0] 
        team2 = rows[i][1] 
        i+=1
         
        if name1 == name2 and team1 == team2:
            break
        # specific case needed since Bryan Gil is named differently in different spreadsheets
        elif name1 == 'Bryan Gil' and name2 == 'Bryan' and team2 == 'TOT':
            break
        elif lastName == name2 and team1 == team2:
            break

    # If name is found
    if i < len(priceData[1]):
        
        price = rows[i-1][3]
        pos = rows[i-1][2]
        
        priceAndPos = (price, pos)
    # If name is not on list   
    else:
        priceAndPos = (100, 'N/A')
    
    return priceAndPos

def getPlayerAvgMinutesFromName(minutesData, name1, team1):
    rows = minutesData[1]
    name2 = ''
    team2 = ''
    names = name1.split(" ")
    lastName = names[-1]

    i = 0
    while i < len(minutesData[1]):
        # Assign name2 = name in the ith row
        
        name2 = rows[i][0] 
        team2 = rows[i][1] 
        i+=1
         
        if name1 == name2 and team1 == team2:
            break
        # specific case needed since Bryan Gil is named differently in different spreadsheets
        elif name1 == 'Bryan Gil' and name2 == 'Bryan' and team2 == 'TOT':
            break
        elif lastName == name2 and team1 == team2:
            break


    avgMins = rows[i-1][2]
    
    return avgMins

Aarray = getProbabilityData('Assist', '7')
Garray = getProbabilityData('Goal', '7')
CSarray = getProbabilityData('Cleansheet', '7')
Parray = getProbabilityData('Price', '7')
Marray = getProbabilityData('Minutes', '7')

a = mergePriceAndMinutesToCSAssistAndGoalData(Aarray, Garray, CSarray, Parray, Marray)
print(a)
# printDataFromArray(Garray,'header')
# printDataFromArray(Garray,'rows')