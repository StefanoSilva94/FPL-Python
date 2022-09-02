'''
Created on 10 Aug 2022
Use this page to get data directly from FPL using publicly available APIs
@author: stefanosilva
'''
import requests
import time



'''
This will take a managers ID and for a specified gameweek and will return an array squad
containing the players chosen by the manager for that gameweek and the FPL Team Per GW API
e.g.:
[[Ward, LEI], [Rpbertson, LIV],...,[Jesus, ARS]]
'''


def getManagerPlayers(managerId, gw):
    gw = str(gw)
    api = 'https://fantasy.premierleague.com/api/entry/' + managerId + '/event/'+ gw + '/picks/'
    response_API = requests.get(api)
    managerData = response_API.json()['picks']    
    squad = []
    # Use the dictionary to map player id to a name and team
    allPlayersDict = createPlayerIDDict()
    for data in managerData:
        playerInfo = data['element']
        squad.append(allPlayersDict[playerInfo])
        
    return squad



def createTeamsDict():
    teamKey = {
        1:'ARS',
        2:'AVL',
        3:'BOU',
        4:'BRE',
        5:'BHA',
        6:'CHE',
        7:'CRY',
        8:'EVE',
        9:'FUL',
        10:'LEI',
        11:'LEE',
        12:'LIV',
        13:'MCI',
        14:'MUN',
        15:'NEW',
        16:"NFO",
        17:'SOU',
        18:'TOT',
        19:'WHU',
        20:'WOL'
    } 

    return teamKey
    

'''
Returns a list, each element of the list contains [player name, team, ID]
Every player in the game is contained in the list
'''
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
        elementID = data[i]['id']
        p.append(elementID)
        # p.append(getPlayerMinutes(str(elementID)))
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


'''
Takes player ID as an input and works out the average minutes per game for this player over a maximum of five games
'''
def getPlayerMinutes(element):
    
    # keep looping until no more APIs can be found. 
    # j is the gameweek index
    i = 0
    j = 0 
    minutes = 0
    
    # Data from 5 matches is needed at maximum, if less than 5 games have been played return avaerage minutes
    while i < 5:
        try:
            playerDetailsAPI = 'https://fantasy.premierleague.com/api/element-summary/'+ element +'/'
            response_API = requests.get(playerDetailsAPI)
            data = response_API.json()['history']
            minutes = minutes + data[j]['minutes']
            j+=1
            i+=1
            
        except:
                # cant divide by 0 so make j non-zero
                if j ==0:
                    j+=1
                    minutes = minutes/j
                    return minutes
                else:
                    minutes = minutes/j
                    return minutes
                    
    return minutes


def getAllPlayersAvgMinutes():
    playerData = getAllPlayerData()
    for player in playerData:
        plID = player[2]
        mins = getPlayerMinutes(str(plID))
        player.append(mins)
        player.pop(2)
        # Adding token 1 to the start of each element in list so that createCSVDataSheets takes consistent format for all lists
        player.insert(0,1)
        # print(player)
    return playerData

# a = getManagerPlayers('3632826','1')

a = getAllPlayerData()
print(a)




