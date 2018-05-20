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
        assert(len(players) == 4)
        
        self.cards, self.target_suit = self.init_cards()
        self.player1 = players[0]
        self.player2 = players[1]
        self.player3 = players[2]
        self.player4 = players[3]
        self.players = players

        self.pot = 0
        self.pot += self.take_antes(self.cards, ante_amt, self.players)
        


    def init_cards(self):
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



    def take_antes(self, deck, ante_amt, players):
        for i in range(len(players)):
            players[i].take(ante_amt)
            #give each 10 cards
            players[i].give_cards(deck[i * 10 : (i + 1) * 10])
            
        return ante_amt * len(players)


    
    def play(self):
        no_trades = 0
        max_no_trades = 9
        
        while no_trades < max_no_trades:
            for i in range(len(self.players)):
                info = self.trade(self.players[i],
                                  self.players[0:i]
                                  + self.players[i + 1:len(self.players)])
                
                if len(info) != 2: no_trades += 1
                
        self.give_rewards()
    
        
    def trade(self, offerer, other_players):
        suit, B, S = offerer.give_proposal()
        offer = (suit, B, S, offerer)
        trade_info = offer
        
        for player in other_players:
            taken = player.consider_proposal(suit, B, S, offerer)
            if taken is None:
                continue
            elif taken is 'Buy': #player wants to buy offerer's card
                card = offerer.take_card_rankless(suit)
                player.give_card(card)
                player.take(S)
                offerer.give(S)
                trade_info = offer, ('Buy', player)
                break
            elif taken is 'Sell': #player to sell their card to the offer
                card = player.take_card_rankless(suit)
                offerer.give_card(card)
                offerer.take(B)
                player.give(S)
                trade_info = offer, ('Sell', player)
                break
            else:
                raise(KeyError) #this situation should never happen by players
            
        return trade_info


    
    def give_rewards(self):
        targets = []
        for player in self.players:
            num_target = len(list(filter((lambda x: x[1] == self.target_suit),
                                         player.cards)))
            player.give(10 * num_target)
            self.pot -= 10 * num_target
            targets.append(num_target)

        #Give the rest of the pot to the player(s) with max target suit
        occ = targets.count(max(targets))
        for i in range(len(self.players)):
            if targets[i] == max(targets):
                self.players[i].give(self.pot / occ)
