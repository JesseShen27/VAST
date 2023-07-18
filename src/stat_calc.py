# Method that calculates average kd for the 4 games
def average_KD(playerInGame):
    totalKills = 0
    totalDeaths = 0
    averageKD = None

    # looping through each of the 4 games and adds to total kills and deaths
    for players in range(4):
        totalKills += playerInGame[players][1]
        totalDeaths += playerInGame[players][2]

    averageKD = totalKills / totalDeaths
    newAverage = round(averageKD, 1)

    return newAverage

# Method that calculates a player's average ADR for the four games
def average_ADR(playerInGame):
    totalADR = 0
    averageADR = None

    # looping through each of the 4 games and adds to total ADR
    for players in range(4):
        totalADR += playerInGame[players][0]

    averageADR = totalADR / 4
    newAverageADR = round(averageADR)

    return newAverageADR

def win_percentage(playerInGame):
    wins = 0

    for players in range(4):
        if (playerInGame[players][3] == 'Won'):
            wins += 1
    
    return wins/4 * 100


