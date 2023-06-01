import requests
from dis_methods import *
from player import Player
from match import Match
from database import Database
import threading
import json
import re

# ------------------- METHODS USED DURING PROCESSING ---------------------------

def set_players_array(players, responseJson, userName):
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

def set_match(players, match, responseJson):
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

    return match

# ------------------------- Grab match history and update json_list ------------------------------------
def fetch_data(url, json_list, json_index):
    json_data = get_match_hisory_json(url)
    json_list[json_index] = json_data


# ----------------------- API CALL -------------------------------------------

def get_match_hisory_json(url):
    response = requests.get(url)
    return response.json()

# ----------------------- BLUE DATABASE SETUP --------------------------------
def set_blue_data(database, json_list, mainMatch):
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
def set_red_data(database, json_list, mainMatch):
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


def process_data(riotID, userRegion):
    # Vars that need to stay constant throughout process loops
    # regex for riot id
    pattern = r"^([A-Za-z0-9 ]{3,16})#([A-Za-z0-9]{3,5})$"
    reg = re.compile(pattern)

    # valid input == 0 if invalid, anything else means valid
    validInput = False

    # checking id validity based on regex
    if not reg.match(riotID):
        return None
    else:
        print("================processing...=================")
        # match group 1 username
        userName = reg.match(riotID).group(1)
        print(userName)
        # match group 2 user tag
        userTag = reg.match(riotID).group(2)
        print(userTag)
        # Riot ID max name length 16 chars
        validInput = True
        # userTag and userName should be good to use now

    # api call for user
    if (validInput != 0):

        print("Setting up data for most recent match...")
  
        json_data = requests.get('https://api.henrikdev.xyz/valorant/v3/matches/'+userRegion+'/'+userName+'/'+userTag+'?filter=competitive')
        responseJson = json_data.json()

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

        set_players_array(players=mainPlayers, responseJson=responseJson, userName=userName)

        mainMatch = Match()

        set_match(players=mainPlayers, match=mainMatch, responseJson=responseJson)
        print("Most recent match set\nSetting up database...")

        # can begin creating database and 9 other API calls
        database = Database()
        database.match = mainMatch

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

        # setting threads list
        threads = []

        # def fetch_data(update, json_cache, url, json_list, json_index):
        t1 = threading.Thread(target = fetch_data, args = (url_list[0], json_list, 0))
        threads.append(t1)
        t2 = threading.Thread(target = fetch_data, args = (url_list[1], json_list, 1))
        threads.append(t2)
        t3 = threading.Thread(target = fetch_data, args = (url_list[2], json_list, 2))
        threads.append(t3)
        t4 = threading.Thread(target = fetch_data, args = (url_list[3], json_list, 3))
        threads.append(t4)
        t5 = threading.Thread(target = fetch_data, args = (url_list[4], json_list, 4))
        threads.append(t5)
        t6 = threading.Thread(target = fetch_data, args = (url_list[5], json_list, 5))
        threads.append(t6)
        t7 = threading.Thread(target = fetch_data, args = (url_list[6], json_list, 6))
        threads.append(t7)
        t8 = threading.Thread(target = fetch_data, args = (url_list[7], json_list, 7))
        threads.append(t8)
        t9 = threading.Thread(target = fetch_data, args = (url_list[8], json_list, 8))
        threads.append(t9)
        t10 = threading.Thread(target = fetch_data, args = (url_list[9], json_list, 9))
        threads.append(t10)

        for x in threads:
            x.start()
            
        for x in threads:
            x.join()

        threads2 = []

        th1 = threading.Thread(target= set_blue_data, args=(database, json_list, mainMatch))
        threads2.append(th1)
        th2 = threading.Thread(target= set_red_data, args=(database, json_list, mainMatch))
        threads2.append(th2)

        # threading finished, json_list is updated and can begin database setting
        for y in threads2:
            y.start()
        
        for y in threads2:
            y.join()

        # database is setup
        return database  