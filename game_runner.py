import player
import game

def main(players):
    g = game.Game(players, 50)
    g.play()

    for i in range(len(players)):
        print("player " + str(i) + " ended with " + str(players[i].coins))



if __name__ == "__main__":
    main([player.Player() for i in range(4)])
