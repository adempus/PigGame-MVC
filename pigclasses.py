from random import randint
import abc
from enum import Enum
import asyncio

class RollInterface(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def snakeEyes(self):
        pass

    @abc.abstractmethod
    def duplicates(self):
        pass


''' Represents a single, six-sided playing die with values from 1 to 6. '''
class Die(object):
    def __init__(self):
        self._faceValue = None      #the resulting value after a roll of this die
        self._minValue = 1
        self._maxValue = 6

    def rollDie(self):
        ''' rolls this die, thus changing its current face value. '''
        self._faceValue = randint(self._minValue, self._maxValue)

    def getValue(self):
        ''' :returns the resulting value from the latest roll of this die.'''
        return self._faceValue

    def __str__(self):
        ''' :returns a string format of the face value '''
        return str(self._faceValue)

    def __add__(self, die):
        ''' :param die - another die whose face value will be added to this one.
            :returns the sum of combined face values from several dice, including this one.
        '''
        return self._faceValue + die.getValue()

    def __eq__(self, die):
        ''' :param die - a die whose face value will be compared with this one.
            :returns True if this die's face value is equal to the specified die's face value.
        '''
        return self._faceValue == die.getValue()


''' Represents a collection of die objects (Dice) to play with. '''
class Dice(RollInterface):
    def __init__(self, numDice):
        ''' :param numDice - the number of dice to include in play. '''
        super().__init__()
        self._numDice = numDice
        self._dice = list()     # a list of face values for the dice rolled
        self._valSum = 0        # a sum of the face values for the rolled dice
        self._initDice()

    def _initDice(self):
        ''' initializes dice for play. '''
        i = 0
        while i < self._numDice:
            self._dice.append(Die())
            i += 1

    def roll(self):
        ''' Rolls a set of dice in play. Basically randomizes values in the list representing dice. '''
        for die in self._dice:
            die.rollDie()

    def snakeEyes(self):
        return (len(self._dice) == 2) and (self._dice[0] == self._dice[1] == 1)

    def duplicates(self):
        if len(self._dice) <= 1: return False
        else:
            return len(list(set(self._dice))) == 1


    def getDice(self):
        ''' :returns a list of integers representing the face values of dice rolls. '''
        return self._dice

    def getValSum(self):
        return sum(self._dice)

    def __str__(self):
        ''' :returns a string representation of dice face values in list format. '''
        stringRep = "["
        for die in self._dice:
            stringRep += str(die)+","
        return stringRep[0:len(stringRep)-1]+"]"

    def __len__(self):
        ''' :returns the number of dice in play'''
        return self._numDice



''' The player class represents a single player in the game. It contains data about the player like their name, and relevant stats. 
'''
class Player(object):
    def __init__(self, name, dice=Dice(1)):
        ''' :param name - the name of the player to display.
            :param dice - playing dice of a specified quantity to be used in-game.
        '''
        self._name = str(name)
        self._dice = dice
        self._turnScore = 0     # a tertiary sum of face values accrued from one or more dice rolls in a single turn.
        self._totalScore = 0    # a permanent sum accumulated from values of previously banked turns.
        self._isWinner = False

    def getName(self):
        ''':returns: the name of this player'''
        return self._name

    def getTurnScore(self):
        return self._turnScore

    def setTurnScore(self, score):
        self._turnScore = score

    def getTotalScore(self):
        return self._totalScore

    def setTotalScore(self, totalScore):
        self._totalScore = totalScore

    def rollDice(self):
        self._dice.roll()

    def getDice(self):
        return self._dice

    def getRollResults(self):
        return self._dice.getDice()

    def bankScore(self):
        ''' "locks in" or adds this player's current turn score to their permanent score. '''
        self._totalScore += self._turnScore

    def resetTotalScore(self):
        ''' resets the total score of this player to zero. '''
        self._totalScore = 0

    def isWinner(self):
        return self._isWinner

    def setWin(self, hasWon):
        self._isWinner = hasWon

    def __str__(self):
        ''' :returns the player's name, total and turn scores, and most recent dice roll face values of this player. '''
        stringRep = "name: "+self._name+"\n"
        stringRep+="total score: "+str(self._totalScore)+"\n"
        stringRep+="turn score: "+str(self._turnScore)+"\n"
        stringRep+="current roll: "+str(self._dice)+"\n"
        return stringRep


class PlayerActions(Enum):
    Roll, Bank = range(2)

class PigGameModel(object):

    ''' PigGameModel represents the model component of the MVC. It contains all data and methods related to the game's logic.
        Ideally, implements a coroutine function to give up control to its caller (the controller), without loosing its state.
    '''
    def __init__(self, numPlayers, scoreCap=50):
        ''' :param *players - a variable amount of players to play the game.
            :param scoreCap - a maximum score at which the game will be triggered to end once a player reaches. Default max is 50
        '''
        self._players = list()
        self._scoreCap = scoreCap
        self._currentPlayerTurn = None                # a reference to the player whose turn it is at the moment.
        self._currentPlayerAction = PlayerActions(0)   # input from current player stored as an action
        self._gameOver = False                       # a flag to indicate the end of the game.
        self._numPlayers = numPlayers                # number of players currently playing
        self._ctrlReference = None                  # a reference to the controller
        self._game = asyncio.get_event_loop()

    def getPlayers(self):
        return self._players

    def getNumPlayers(self):
        return self._numPlayers

    def declareNewPlayer(self, playerName):
        ''' adds a new player to the current game
            :param playerName - the name of the player to add to this game.
        '''
        newPlayer = Player(playerName, Dice(2))
        self._setPlayers(newPlayer)


    def _setPlayers(self, *players):
        ''' utility method for adding a new player to this game's list of players.
            :param a variable number of player objects to initialize the game with.
        '''
        for player in players:
            self._players.append(player)

    def setControl(self, controller):
        self._ctrlReference = controller

    def updatePlayerAction(self, action=None):
        self._currentPlayerAction = action

    def startGame(self):
        self._changePlayerTurn()
        self._game.run_until_complete(self._gameLoop())
        self._endGame()

    def _endGame(self):
        self._game.close()

    async def _gameLoop(self):
        ''' a coroutine function that drives the game's loop, and doubles as an event loop;
            changing game state, based on input delegated from the controller. '''
        while self._gameOver is False:
            playerIn = self._ctrlReference.getInput()
            print(str(playerIn))
            self._checkInput(playerIn)
            self._performPlayerAction()
            #TODO: complete the loop

    def checkForWinner(self):
        ''' periodically checks at the end of a player's turn, if a win condition has been met. '''
        #TODO: Find out if lambdas to stream/filter players would make this more efficient. Loop can cause O(n^2) runtime.
        for player in self._players:
            if player.getTotalScore() >= self._scoreCap:
                player.setWin(True)
                self._gameOver = True
                return

    def _checkInput(self, playerIn):
        if str(playerIn).upper() is "R":
            self._currentPlayerAction = PlayerActions.Roll
            return
        elif str(playerIn).upper() is "B":
            self._currentPlayerAction = PlayerActions.Bank
            return

    def _performPlayerAction(self):
        if self._currentPlayerAction is PlayerActions.Roll:
            self._currentPlayerTurn.rollDice()
            print("rolled: "+str(self._currentPlayerTurn.getDice()))

    def setScoreCap(self, maxScore):
        self._scoreCap = maxScore


    def _changePlayerTurn(self):
        ''' sets the current turn to the next player in the list of in-game players. '''
        self._currentPlayerTurn = self._players.pop(0)
        self._players.append(self._currentPlayerTurn)

    def getCurrentPlayerTurn(self):
        return self._currentPlayerTurn

