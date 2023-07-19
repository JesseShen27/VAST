# Method that calculates average kd for the 4 games
def average_KD(playerInGame):
    totalKD = 0.0
    # looping through each of the 4 games and adds to total kills and deaths
    for players in range(4):
        kills = playerInGame[players][1]
        deaths = playerInGame[players][2]
        totalKD += kills/deaths
        
    return totalKD/4

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

def get_red_kd_avg(playerArr, userIndex):
    totalKd = 0.0
    userTeam = False
    for i in range(5,10):
        if (i == userIndex):
            userTeam = True
            continue
        totalKd += average_KD(playerArr[i])
    if (userTeam):
        redTeamAvg  = round(totalKd/4, 2)
    else:
        redTeamAvg = round(totalKd/5, 2)
    return redTeamAvg


def get_blue_kd_avg(playerArr, userIndex):
    totalKd = 0.0
    userTeam = False
    for i in range(5):
        if (i == userIndex):
            userTeam = True
            continue
        totalKd += average_KD(playerArr[i])
    if (userTeam):
        blueTeamAvg  = round(totalKd/4, 2)
    else:
        blueTeamAvg = round(totalKd/5, 2)
    return blueTeamAvg
