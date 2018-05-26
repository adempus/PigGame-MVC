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

    def alertPlayerDouble(self, playerName):
        alert = playerName+" "+self._doubleAlert+"\n"
        alert += playerName+" must re-roll without banking. "
        print(alert)

    def alertEndTurn(self, playerName):
        print(playerName+self._endTurnAlert)

