'''
Created on 10 Aug 2022
Use this page to get data directly from FPL using publicly available APIs
@author: stefanosilva
'''
import requests


'''
This will take a managers ID and for a specified gameweek and will return an array squad
containing the players chosen by the manager for that gameweek and the FPL Team Per GW API
'''


def getManagerPlayers(managerId, gw):
    api = 'https://fantasy.premierleague.com/api/entry/' + managerId + '/event/'+ gw + '/picks/'
    response_API = requests.get(api)
    managerData = response_API.json()['picks']    
    squad = []
    # Use the dictionary to map player id to a name and team
    allPlayersDict = createPlayerIDDict()
    for data in managerData:
        playerInfo = data['element']
        squad.append(allPlayersDict[playerInfo])
        
    
    # print(squad)  
    return squad

def createTeamsDict():
    teamKey = {
        1:'Arsenal',
        2:'Aston Villa',
        3:'Bournemouth',
        4:'Brentford',
        5:'Brighton',
        6:'Chelsea',
        7:'Crystal Palace',
        8:'Everton',
        9:'Fulham',
        10:'Leicester',
        11:'Leeds',
        12:'Liverpool',
        13:'Man City',
        14:'Man Utd',
        15:'Newcastle',
        16:"Nott'm Forest",
        17:'Southampton',
        18:'Spurs',
        19:'West Ham',
        20:'Wolves'
    } 

    return teamKey
    

def getAllPlayerData():
    response_API = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = response_API.json()['elements']
    players = []
    teamKey = createTeamsDict()
    for i in range(0, len(data)):
        p = []
        p.append(data[i]['web_name'])
        teamID = (data[i]['team'])
        p.append(teamKey[teamID])
        p.append(data[i]['id'])
        players.append(p)
        
          
    return players


def createPlayerIDDict():
    playerKey = {}
    '''
    players is an multi dim array
    players [i][0] of each array is player name as shown on FPL
    players [i][1] of each array is the players team
    players [i][2] is the players ID
    '''
    players  = getAllPlayerData()
    
    for player in players:
        name = player[0]
        team = player[1]
        playerId = player[2]
        
        
        playerKey[playerId] = [name, team]
    
    return playerKey


# getManagerPlayers('3632826','1')


