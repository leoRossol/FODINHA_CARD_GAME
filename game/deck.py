import random
from .card import Card

class Deck:

    def __init__(self):
        values = list(range(2,15))
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades' ]
        self.cards = [Card(value, suit) for value in values for suit in suits]
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.cards)


    def draw(self):
        return self.cards.pop() if self.cards else None