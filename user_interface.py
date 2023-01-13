import requests
from player import Player
from match import Match
import json
import ctypes

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

    players = [player1, player2, player3, player4, player5 ,player6 ,player7 ,player8 ,player9 ,player10]

    for playerIndex in range(10):
        if (responseJson['data'][0]['players']['all_players'][playerIndex]['name'] == userName):
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
        
    for i in range(10):
        print("player", i + 1, ": " + str(players[i]))