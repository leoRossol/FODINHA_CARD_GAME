from .deck import Deck
from .player import Player

class Game:

    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]


    def start(self):
        #ADD LOGIC LATER XD
        pass