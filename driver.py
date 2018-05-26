from pigclasses import PigGameModel
from view import PigGameView
from controller import PigGameController

player1 = object()
player2 = object()
pigGameModel = object()
pigGameView = object()
pigGameCtrl = object()


def main():
    gameModel = PigGameModel(2)
    pigGameView = PigGameView()
    pigGameCtrl = PigGameController(gameModel, pigGameView)
    pigGameCtrl.initGame()

    print("--current players--\n")
    for player in pigGameCtrl.getPlayers():
        print(player)

main()
