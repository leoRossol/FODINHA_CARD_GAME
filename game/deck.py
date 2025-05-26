import random
from .card import Card

class Deck:

    def __init__(self):
        values = [4,5,6,7,11,12,13,14,15,16]
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades' ]
        self.cards = [Card(value, suit) for value in values for suit in suits]
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.cards)


    def draw(self):
        return self.cards.pop() if self.cards else None