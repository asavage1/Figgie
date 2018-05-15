import player
import game

def main(players):
    g = game.Game(players, 50)
    g.play()

    for i in range(len(players)):
        print("player " + i + " ended with " players[i].coins)



if __name__ == "__main__":
    main(players)
    #main([player.Player() for i in range(3)] + [player.SimpleTargetPlayer()])
