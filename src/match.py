class Match:

    def __init__(self):
        # two arrays of size 5 representing team players in each index
        self.blueTeam = [None] * 5
        self.redTeam = [None] * 5

        # String that will represent the team color of the user
        self.userTeamColor = None

        # variable that stores the index of the player
        self.userIndex = None
    
    def arrayToString(s) :
        # method to convert an array to a string format
        str1 = ""

        for element in s :
            str1 += ' ' + element

        return str1

    # Printing out the sorted teams by blue and red
    def __str__(self):
        finalString = "Blue Team: \n"
        for element in self.blueTeam :
            finalString += str(element) + "\n"
        finalString += "Red Team: \n"
        for element in self.redTeam :
            finalString += str(element) + " \n"
        return f'User Team Color is: {self.userTeamColor}\nUser index in specific array: {self.userIndex}\n{finalString}'