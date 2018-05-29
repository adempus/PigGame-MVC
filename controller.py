''' The PigGameController class is responsible for delegating input from the user to the model to change the model's state.
    It in turn updates the state of the view, and invokes view's functions for displaying prompts and alerts to the console.
'''
class PigGameController(object):
    def __init__(self, model, view):
        ''' :param model - is a reference where the game's logic is sored.
            :param view - is a reference where the game's output contents are stored. '''
        self._gameModel = model
        self._gameModel.setControl(self)
        self._gameView = view

    def getPlayers(self):
        ''' :returns the players currently in game from the model. '''
        return self._gameModel.getPlayers()

    def initGame(self):
        '''sets the game up, then starts it. '''
        for count in range(1, self._gameModel.getNumPlayers()+1):
            self._gameView.promptPlayerName(count)
            self._gameModel.declareNewPlayer(str(input()))
        self._gameModel.startGame()


    #TODO figure out coordination between this method and the model's game loop
    def getInput(self):
        #TODO if statements to split up view displays with corresponding model states; for input.
        '''retrieves player input from the console.'''
        self._gameView.promptPlayerGo(
            self._gameModel.getCurrentPlayerTurn().getName()
        )
        option = str(input())
        return option

    #TODO
    def endGame(self):
        ''' ends the current game'''
        pass


