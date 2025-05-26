class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bet = 0
        self.tricks_won = 0
        self.score = 0


    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card