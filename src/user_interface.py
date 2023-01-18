import requests
from om_methods import *
from player import Player
from match import Match
from database import Database
import threading
import json

# ------------------- METHODS USED DURING PROCESSING ---------------------------

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

# ------------------------- CACHE METHOD ------------------------------------
def fetch_data(update, json_cache, url, json_list, json_index):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache, 'r') as file:
                json_data = json.load(file)
                print('Fetched data from local cache')
        except(FileNotFoundError, json.JSONDecodeError) as e:
            print(f'No local cache found... ({e})')
            json_data = None
    
    if not json_data:
        print('Fetching new json data... (Updating local cache)')
        json_data = get_match_hisory_json(url)
        with open(json_cache, 'w') as file:
            json.dump(json_data, file)
    
    json_list[json_index] = json_data


# ----------------------- API CALL -------------------------------------------

def get_match_hisory_json(url):
    response = requests.get(url)
    return response.json()

# ----------------------- BLUE DATABASE SETUP --------------------------------
def set_blue_data(database, json_list):
    for playerIndex in range(5):

        currentPuuid = mainMatch.blueTeam[playerIndex].puuid
        responseJson = json_list[playerIndex]

        for tmpMatchIndex in range (1, 5):
                for tmpPlayerIndex in range (10):
                    if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['puuid'] == currentPuuid):
                        if (playerIndex == 0):
                            database.b1[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b1[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b1[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b1[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b1[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b1[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b1[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b1[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b1[tmpMatchIndex - 1][3] = "Draw"
                            
                        elif (playerIndex == 1):
                            database.b2[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b2[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b2[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b2[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b2[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b2[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b2[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b2[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b2[tmpMatchIndex - 1][3] = "Draw"
                            
                        elif (playerIndex == 2):
                            database.b3[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b3[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b3[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b3[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b3[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b3[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b3[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b3[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b3[tmpMatchIndex - 1][3] = "Draw"
                            
                        elif (playerIndex == 3):
                            database.b4[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b4[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b4[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b4[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b4[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b4[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b4[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b4[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b4[tmpMatchIndex - 1][3] = "Draw"
                            
                        else:
                            database.b5[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']), 1)
                            database.b5[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.b5[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b5[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.b5[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b5[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b5[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.b5[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.b5[tmpMatchIndex - 1][3] = "Draw"    
                            
# ----------------------- RED DATABASE SETUP --------------------------------
def set_red_data(database, json_list):
    for playerIndex in range(5):
        
        responseJson = json_list[playerIndex + 5]
        currentPuuid = mainMatch.redTeam[playerIndex].puuid
            
        for tmpMatchIndex in range (1, 5):
                for tmpPlayerIndex in range (10):
                    if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['puuid'] == currentPuuid): 
                        if (playerIndex == 0):
                            database.r1[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r1[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r1[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r1[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r1[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r1[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r1[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r1[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r1[tmpMatchIndex - 1][3] = "Draw"
                            
                        elif (playerIndex == 1):
                            database.r2[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r2[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r2[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r2[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r2[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r2[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r2[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r2[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r2[tmpMatchIndex - 1][3] = "Draw"
                            
                        elif (playerIndex == 2):
                            database.r3[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r3[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r3[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r3[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r3[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r3[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r3[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r3[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r3[tmpMatchIndex - 1][3] = "Draw"
            
                        elif (playerIndex == 3):
                            database.r4[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r4[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r4[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r4[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r4[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r4[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r4[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r4[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r4[tmpMatchIndex - 1][3] = "Draw"

                        else:
                            database.r5[tmpMatchIndex - 1][0] = round(responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['damage_made'] / (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] + responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']), 1)
                            database.r5[tmpMatchIndex - 1][1] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['kills']
                            database.r5[tmpMatchIndex - 1][2] = responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['stats']['deaths']
                            if (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Blue"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r5[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['blue']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['blue']['rounds_lost']):
                                    database.r5[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r5[tmpMatchIndex - 1][3] = "Draw"
                            elif (responseJson['data'][tmpMatchIndex]['players']['all_players'][tmpPlayerIndex]['team'] == "Red"):
                                if (responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_won'] > responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r5[tmpMatchIndex - 1][3] = "Won"
                                elif (responseJson['data'][tmpMatchIndex]['teams']['red']['has_won'] < responseJson['data'][tmpMatchIndex]['teams']['red']['rounds_lost']):
                                    database.r5[tmpMatchIndex - 1][3] = "Lost"
                                else:
                                    database.r5[tmpMatchIndex - 1][3] = "Draw"
# --------------------------- METHODS END -------------------------------------


# --------------------- PROCESSING BEGINS HERE --------------------------------

# Vars that need to stay constant throughout process loops
processContinue = True
lastUserName: str = None
lastUserTag: str = None
user_cache_json = 'cache/data0user.json'
while (processContinue):
    # First task is to ask for user Information
    userInput = input("Enter Riot ID (\"example#0000\") or 'quit': ")
    if (userInput == "quit"):
        processContinue = False
        exit()
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
        # userTag and userName should be good to use now


    # api call for user

    if (validInput != 0):

        # caching first API call
        if ((userTag != lastUserTag) or (userName != lastUserName)):
            json_data = None
        else:
            try:
                with open(user_cache_json, 'r') as file:
                    json_data_orig = json.load(file)
                    print('Fetched data from local cache')
            except(FileNotFoundError, json.JSONDecodeError) as e:
                print(f'No local cache found... ({e})')
                json_data_orig = None
    
        if not json_data:
            print('Fetching new json data... (Updating local cache)')
            json_data = requests.get('https://api.henrikdev.xyz/valorant/v3/matches/'+userRegion+'/'+userName+'/'+userTag+'?filter=competitive')
            json_data = json_data.json()
            with open(user_cache_json, 'w') as file:
                json.dump(json_data, file)

        responseJson = json_data

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
        url_list = [None] * 10
        
        # settting URL list
        for playerIndex in range(10):
            if (playerIndex <= 4):
                url = 'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/'+userRegion+'/'+mainMatch.blueTeam[playerIndex].puuid+'?filter=competitive'
                url_list[playerIndex] = url
            else:
                url = 'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/'+userRegion+'/'+mainMatch.redTeam[playerIndex - 5].puuid+'?filter=competitive'
                url_list[playerIndex] = url

        
        json_list = [None] * 10

        json_cache1 = 'cache/data01.json'
        json_cache2 = 'cache/data02.json'
        json_cache3 = 'cache/data03.json'
        json_cache4 = 'cache/data04.json'
        json_cache5 = 'cache/data05.json'
        json_cache6 = 'cache/data06.json'
        json_cache7 = 'cache/data07.json'
        json_cache8 = 'cache/data08.json'
        json_cache9 = 'cache/data09.json'
        json_cache10 = 'cache/data10.json'

        # need something that determines whether or not we want update probably want this to update every 10 minutes or something
        update: bool = False
        if ((lastUserName == userName) and (lastUserTag == userTag)):
            update = False
        else:
            update = True

        # setting threads list
        threads = []

        # def fetch_data(update, json_cache, url, json_list, json_index):
        t1 = threading.Thread(target = fetch_data, args = (update, json_cache1, url_list[0], json_list, 0))
        threads.append(t1)
        t2 = threading.Thread(target = fetch_data, args = (update, json_cache2, url_list[1], json_list, 1))
        threads.append(t2)
        t3 = threading.Thread(target = fetch_data, args = (update, json_cache3, url_list[2], json_list, 2))
        threads.append(t3)
        t4 = threading.Thread(target = fetch_data, args = (update, json_cache4, url_list[3], json_list, 3))
        threads.append(t4)
        t5 = threading.Thread(target = fetch_data, args = (update, json_cache5, url_list[4], json_list, 4))
        threads.append(t5)
        t6 = threading.Thread(target = fetch_data, args = (update, json_cache6, url_list[5], json_list, 5))
        threads.append(t6)
        t7 = threading.Thread(target = fetch_data, args = (update, json_cache7, url_list[6], json_list, 6))
        threads.append(t7)
        t8 = threading.Thread(target = fetch_data, args = (update, json_cache8, url_list[7], json_list, 7))
        threads.append(t8)
        t9 = threading.Thread(target = fetch_data, args = (update, json_cache9, url_list[8], json_list, 8))
        threads.append(t9)
        t10 = threading.Thread(target = fetch_data, args = (update, json_cache10, url_list[9], json_list, 9))
        threads.append(t10)

        for x in threads:
            x.start()
            
        for x in threads:
            x.join()

        threads2 = []

        th1 = threading.Thread(target= set_blue_data, args=(database, json_list))
        threads2.append(th1)
        th2 = threading.Thread(target= set_red_data, args=(database, json_list))
        threads2.append(th2)

        # threading finished, json_list is updated and can begin database setting

        for y in threads2:
            y.start()
        
        for y in threads:
            y.join()

        database.data_print()

        lastUserName = userName
        lastUserTag = userTag
        # database is setup

        # BEGIN MATH METHODS

    


