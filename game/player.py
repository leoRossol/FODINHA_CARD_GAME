class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []


    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card