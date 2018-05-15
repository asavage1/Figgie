"""
The setup for the game, initializing players and such.

--------------------------
Game:
Deck of cards, 40 made up of 12, 10, 10, 8 of each suit-suits chosen randomly
Whatever suit is the same color as the suit with 12 is the target suit 
(not inc the 12).

Each player (4 of them) pays 50 coins to the pot to get 10 cards
Then, they can buy and sell cards as they please until all are done

At the end, each player gets 10 coins from the pot for each target card in 
their hand, and the person with the most target cards gets the rest of the pot (
it’s split in the case of the tie)
--------------------------

"""


import player
import random

class Game(object):
    def __init__(self, players, ante_amt):
        #assert(len(players) == 4)
        
        self.cards, self.target_suit = init_cards()
        self.player1 = players[0]
        self.player2 = players[1]
        self.player3 = players[2]
        self.player4 = players[3]

        self.pot = 0
        self.pot += take_antes(ante_amt)
        


    def init_cards():
        suits = ['Clubs', 'Hearts', 'Spades', 'Diamonds']
        random.shuffle(suits)
        ranks = [(i + 1) for i in range(13)]
        deck = []

        target = ''
        if   suits[0] == 'Clubs'   : target = 'Spades'
        elif suits[0] == 'Spades'  : target = 'Clubs'
        elif suits[0] == 'Diamonds': target = 'Hearts'
        elif suits[0] == 'Hearts'  : target = 'Diamonds'

        for n, suit in zip([12, 10, 10, 8], suits):
            # List of tuples in form (rank, suit) containing 12,10,10,8 of each
            deck += list(zip(random.sample(ranks, k=n), [suit] * n))
        random.shuffle(deck)

        return deck, target



    def take_antes(ante_amt):
        for i in range(len(players)):
            players[i].take(ante_amt)
            #give each 10 cards
            players[i].give_cards(deck[i * 10 : (i + 1) * 10])
            
        return ante_amt * len(players)


    
    def play():
        trade()
        give_rewards()


        
    def trade():
        pass


    
    def give_rewards():
        targets = []
        for player in players:
            num_target = len(list(filter((lambda x: x[1] == target),
                                         player.cards)))
            player.give(10 * num_target)
            self.pot -= 10 * num_target
            targets.append(num_target)

        #Give the rest of the pot to the player(s) with max target suit
        occ = targets.count(max(targets))
        for i in range(len(players)):
            if targets[i] == max(targets):
                players[i].give(self.pot / occ)
