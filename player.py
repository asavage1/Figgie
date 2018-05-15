"""
Base player class
"""


class Player(object):    
    def __init__(self):
        self.coins = 0
        self.cards = []
        
    def take(self, amt):
        self.coins -= amt

    def give(self, amt):
        self.coins += amt

    def give_cards(self, cards):
        self.cards += cards

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

    # Based on the strategy, implemented in extensions
    def give_proposal(self):
        pass

    def consider_proposal(self, suit, B, S, playerID):
        pass


    
class BoringPlayer(Player):
    def get_moves(self):
        return [X,X,X,X]

class SimpleTargetPlayer(Player):
    def get_moves(self):
        suit_occ = {}
        for s in suits:
            suit_occ[s] = 0
        for r,s in self.cards:
                suit_occ[s] += 1
        target = max(suit_occ, key=suit_occ.get)

        moves = []
        for suit in suits:
            if suit == target:
                moves.append(10)
            else:
                moves.append(-5)
            
        return moves
