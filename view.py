''' This class encapsulates common in-game messages to show on screen, and houses functions in the form of alerts and
    prompts for showing the corresponding in-game messages when called upon by the controller class.
'''
class PigGameView(object):
    def __init__(self):
        self._playerNamePrompt = str()
        self._rollOrBankPrompt = "Enter 1: Roll again, Enter 2: bank score"
        self._snakeEyesAlert = "Snake Eyes!"
        self._pigAlert = "is PIG!"
        self._doubleAlert = "rolled double!"
        self._endTurnAlert = "turn has ended."

    def promptPlayerName(self, playerId):
        self._playerNamePrompt = "Player "+str(playerId)+" enter name: "
        print(self._playerNamePrompt)

    def alertPlayerIsPig(self, playerName):
        alert = playerName+" "+self._pigAlert
        print(alert)

    def promptPlayerBank(self, playerObj):
        prompt = "Bank "+playerObj.getTurnScore()+" to total score?"
        print(prompt)

    def promptPlayerGo(self, playerName):
        ''' prints a textual alert for the player whose turn it is. '''
        alert = "It's "+str(playerName)+"\'s turn. Enter \'R\' to roll dice."
        print(alert)

    def viewPlayerStats(self, playerObj):
        ''':param playerObj - an object of the player currently in play. '''
        print(str(playerObj))

    def viewPlayerRollResult(self, playerObj):
        ''' :param playerObj - the player whom to see results for. '''
        result = playerObj.getName()+" rolled: "+str(playerObj.getDice())+"\nturn total = "+str(playerObj.getRollTotal())
        print(result)

    def alertPlayerDouble(self, playerObj):
        ''' :param playerObj - the player whom to alert when they've rolled a non-snake eyes double value. '''
        alert = playerObj.getName()+" "+self._doubleAlert+"\n"
        alert += playerObj.getName()+" must re-roll without banking. "
        print(alert)



    def alertEndTurn(self, playerName):
        print(playerName+self._endTurnAlert)

