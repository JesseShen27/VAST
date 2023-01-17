import requests
from player import Player
from match import Match
from database import Database
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import ctypes

def set_players_array(players):
     for playerIndex in range(10):
        if (responseJson['data'][0]['players']['all_players'][playerIndex]['name'] == userName and responseJson['data'][0]['players']['all_players'][playerIndex]['tag']):
            players[playerIndex].isUser = True
            players[playerIndex].deaths = responseJson['data'][0]['players']['all_players'][playerIndex]['stats']['deaths']
            players[playerIndex].kills = responseJson['data'][0]['players']['all_players'][playerIndex]['stats']['kills']
            players[playerIndex].puuid = responseJson['data'][0]['players']['all_players'][playerIndex]['puuid']
            players[playerIndex].teamColor = responseJson['data'][0]['players']['all_players'][playerIndex]['team']
        else:
            players[playerIndex].isUser = False
            players[playerIndex].deaths = responseJson['data'][0]['players']['all_players'][playerIndex]['stats']['deaths']
            players[playerIndex].kills = responseJson['data'][0]['players']['all_players'][playerIndex]['stats']['kills']
            players[playerIndex].puuid = responseJson['data'][0]['players']['all_players'][playerIndex]['puuid']
            players[playerIndex].teamColor = responseJson['data'][0]['players']['all_players'][playerIndex]['team']

def set_match(players, match):
    # Beginning match setup
    blueCount = 0
    redCount = 0
    roundsWon = None
    roundsLost = None

    # Looping through players
    for matchIndex in range(10):
        if (players[matchIndex].teamColor == "Blue") :
            match.blueTeam[blueCount] = players[matchIndex]
            if (players[matchIndex].isUser == True) :
                match.userTeamColor = "blue"
                match.userIndex = blueCount
            blueCount += 1
        else:
            match.redTeam[redCount] = players[matchIndex]
            if (players[matchIndex].isUser == True) :
                match.userTeamColor = "red"
                match.userIndex = redCount
            redCount += 1                 
    
    if (match.userTeamColor == "blue"):
        roundsLost = responseJson['data'][0]['teams']['blue']['rounds_lost']
        roundsWon = responseJson['data'][0]['teams']['blue']['rounds_won']
    else:
        roundsLost = responseJson['data'][0]['teams']['red']['rounds_lost']
        roundsWon = responseJson['data'][0]['teams']['red']['rounds_won']

    if (roundsLost > roundsWon):
        match.userWinLoss = "Loss"
    elif (roundsWon > roundsLost):
        match.userWinLoss = "Win"
    elif (roundsWon == roundsLost):
        match.userWinLoss = "Draw"

    print(match)
    return match


def set_blue_data(database):
    for playerIndex in range(5):
        if (mainMatch.blueTeam[playerIndex].isUser == True):
            continue
        else:
            response = requests.get('https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/'+userRegion+'/'+mainMatch.blueTeam[playerIndex].puuid+'?filter=competitive')

            responseJson = response.json()

            currentPuuid = mainMatch.blueTeam[playerIndex].puuid
            
            for tmpMatchIndex in range (1, 5):
                for tmpPlayerIndex in range (10):
                    if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['puuid'] == currentPuuid):
                        if (playerIndex == 0):
                            database.b1[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b1[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b1[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b1[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b1[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.b1[tmpMatchIndex - 1][3] = "Draw"
                            database.b1[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 1):
                            database.b2[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b2[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b2[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b2[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b2[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.b2[tmpMatchIndex - 1][3] = "Draw" 
                            database.b2[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 2):
                            database.b3[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b3[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b3[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b3[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b3[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.b3[tmpMatchIndex - 1][3] = "Draw"
                            database.b3[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 3):
                            database.b4[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b4[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b4[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b4[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b4[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.b4[tmpMatchIndex - 1][3] = "Draw"
                            database.b4[tmpMatchIndex - 1][4] = False
                        else:
                            database.b5[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b5[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b5[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b5[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                database.b5[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.b5[tmpMatchIndex - 1][3] = "Draw"
                            database.b5[tmpMatchIndex - 1][4] = False

def set_red_data(database):
    for playerIndex in range(5):
        if (mainMatch.redTeam[playerIndex].isUser == True):
            continue
        else:
            response = requests.get('https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/'+userRegion+'/'+mainMatch.redTeam[playerIndex].puuid+'?filter=competitive')

            responseJson = response.json()

            currentPuuid = mainMatch.redTeam[playerIndex].puuid
            
            for tmpMatchIndex in range (1, 5):
                for tmpPlayerIndex in range (10):
                    if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['puuid'] == currentPuuid): 
                        if (playerIndex == 0):
                            database.r1[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r1[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r1[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r1[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r1[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.r1[tmpMatchIndex - 1][3] = "Draw"
                            database.r1[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 1):
                            database.r2[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r2[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r2[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r2[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r2[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.r2[tmpMatchIndex - 1][3] = "Draw"
                            database.r2[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 2):
                            database.r3[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r3[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r3[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r3[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r3[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.r3[tmpMatchIndex - 1][3] = "Draw"
                            database.r3[tmpMatchIndex - 1][4] = False
                        elif (playerIndex == 3):
                            database.r4[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r4[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r4[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r4[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r4[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.r4[tmpMatchIndex - 1][3] = "Draw"
                            database.r4[tmpMatchIndex - 1][4] = False
                        else:
                            database.r5[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r5[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r5[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r5[tmpMatchIndex - 1][3] = "Won"
                            elif (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                database.r5[tmpMatchIndex - 1][3] = "Lost"
                            else:
                                database.r5[tmpMatchIndex - 1][3] = "Draw"
                            database.r5[tmpMatchIndex - 1][4] = False

def runner():
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        threads.append(executor.submit(set_blue_data,database))
        threads.append(executor.submit(set_red_data,database))

# First task is to ask for user Information
userInput = input("Enter Riot ID (\"example#0000\"): ")
userRegion = input("Enter Region: (na, eu, ap, kr): ")

# valid input == 0 if invalid, anything else means valid

validInput = False

if (len(userInput) > 22 or len(userInput) < 8):
    print("Invalid Riot ID")
else:
    # Riot ID max name length 16 chars
    userName = ("%" * 16)
    # Riot ID max tag length 5 chars
    userTag = ("%" * 5)

    # Necessary Index values for string manipulation of tag and username
    tagIndex = 0
    nameIndex = 0
    #loops through string looking for '#'
    for i in range(len(userInput)):
        # found '#' begin placing characters in tag
        if (userInput[i] == "#"):
            # loop to place characters from input into tag string
            for j in range(len(userInput) - i - 1):
                # if to check for last index
                if (i == len(userInput) - 1):
                    break
                else:
                    userTag = userTag[:tagIndex] + userInput[i + j + 1] + userTag[tagIndex:]
                    tagIndex += 1
            break
        # Otherwise place characters from input in username
        else:
            userName = userName[:nameIndex] + userInput[i] + userName[nameIndex:]
            nameIndex += 1

    userTag = userTag.strip("%")
    userName = userName.strip("%")
    validInput = True

    print("\"" + userName + "\"")
    print("\"" + userTag + "\"")
    print("\"" + userRegion + "\"")


    # userTag and userName should be good to use now


# api call for user

if (validInput != 0):

    response = requests.get('https://api.henrikdev.xyz/valorant/v3/matches/'+userRegion+'/'+userName+'/'+userTag+'?filter=competitive')

    responseJson = response.json()

    player1 = Player()
    player2 = Player()
    player3 = Player()
    player4 = Player()
    player5 = Player()
    player6 = Player()
    player7 = Player()
    player8 = Player()
    player9 = Player()
    player10 = Player()
    mainPlayers = [player1, player2, player3, player4, player5 ,player6 ,player7 ,player8 ,player9 ,player10]

    set_players_array(players=mainPlayers)

    mainMatch = Match()

    set_match(players=mainPlayers, match=mainMatch)

    # can begin creating database and 9 other API calls
    database = Database()

    runner()


    
    print(database.b1)
    print(database.b2)
    print(database.b3)
    print(database.b4)
    print(database.b5)
    print("=====================================================================================================================================================")
    print(database.r1)
    print(database.r2)
    print(database.r3)
    print(database.r4)
    print(database.r5)
            
