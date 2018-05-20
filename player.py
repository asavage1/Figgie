"""
Base player class
"""


class Player(object):    
    def __init__(self):
        self.coins = 0
        self.cards = []
        self.seen_cards = []
        self.seen_suits = {'Diamonds': 0, 'Clubs': 0, 'Hearts': 0, 'Spades': 0}
        
    def take(self, amt):
        self.coins -= amt

    def give(self, amt):
        self.coins += amt

    def give_card(self, card):
        self.cards += [card]
        update_seen(self, [card])
        
    def give_cards(self, cards):
        self.cards += cards
        self.update_seen(cards)

    def update_seen(self, cards):
        for card in cards:
            if not card in self.seen_cards:
                self.seen_cards += [card]
                self.seen_suits[card[1]] += 1
        
    def take_cards(self, cards):
        for card in cards:
            if card not in self.cards:
                return False
        for card in cards:
            take_card(card)
        return True

    def take_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else: return False



    def take_card_rankless(self, suit):
        suited_cards = filter(lambda x: x[1] == suit, self.cards)
        if len(suited_cards) is not 0:
            return suited_cards[0]
    

    # Based on the strategy, implemented in extensions
    def give_proposal(self):
        return 1,2,2

    def consider_proposal(self, suit, B, S, playerID):
        pass
    
