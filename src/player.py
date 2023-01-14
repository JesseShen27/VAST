class Player:

    def __init__(self):
        self.puuid = None
        self.kills = None
        self.deaths = None
        self.teamColor = None
        self.isUser = False


    def __str__(self):
        return f'puuid: {self.puuid}, kills: {self.kills}, deaths: {self.deaths}, teamColor: {self.teamColor}, isUser: {self.isUser}'
