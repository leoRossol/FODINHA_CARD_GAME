from .deck import Deck
from .player import Player

CARD_ORDER = [
    (4, None),
    (5, None),
    (6, None),
    (7, None),
    (12, None),
    (13, None),
    (14, None),
    (15, None),
    (16, None),
    (7, 'Diamonds'),
    (7, 'Spades'),
    (14, 'Clubs'),
    (14, 'Spades')
]

def card_rank(card):
    for i, (value, suit) in enumerate(CARD_ORDER):
        if card.value == value and (suit is None or card.suit == suit):
            return i
    return -1


class Game:

    def __init__(self, player_names):

        #check if the game has four players
        if len(player_names) != 4:
            raise ValueError("THE GAME NEEDS 4 PLAYERS TO BEGIN")

        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.round = 1
        self.dealer_index = 0

    def start(self):
        while not self.game_over():
            self.play_round()
            self.round += 1
            self.dealer_index = (self.dealer_index + 1) % 4

    def play_round(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_cards()

        self.reveal_cards()
        self.collect_bets()

        for player in self.players:
            player.tricks_won = 0

        starting_player = (self.dealer_index + 1) % 4
        for _ in range(self.round):
            winner = self.play_trick(starting_player)
            starting_player = self.players.index(winner)

        self.update_scores()
        self.dealer_index = (self.dealer_index + 1) % 4

    def deal_cards(self):
        for player in self.players:
            player.hand = []  #clear the player hand

            #for loop draws n of cards equal to the round
            for _ in range(self.round):
                card = self.deck.draw()
                if card:
                    player.hand.append(card)

    #TODO - REPLACE THE PRINT STATEMENTS WITH ACTUAL DISPLAY LOGIC
    def reveal_cards(self):
        if self.round == 1:
            # First round: everyone sees all cards except their own
            for player in self.players:
                visible_cards = {p.name: p.hand[0] for p in self.players if p != player}
                # Here, display `visible_cards` to `player`
                # and hide their own card from them
                print(f"{player.name} sees: {visible_cards}")
        else:
            # Other rounds: each player sees only their own cards
            for player in self.players:
                print(f"{player.name} sees their cards: {player.hand}")

    # TODO - REPLACE THE PRINT STATEMENTS WITH ACTUAL DISPLAY LOGIC
    def collect_bets(self):
        bets = [None] * 4

        for i in range(4):
            player_index = (self.dealer_index + 1 + i) % 4
            player = self.players[player_index]

            #replace input() with ui logic
            bet = int(input(f"{player.name}, place your bet: "))
            bets[player_index] = bet

            #last player must ensure total bets != round
            if i == 3 and sum(bets) == self.round:
                print("total bets == n of rounds")
                while True:
                    bet = int(input(f"{player.name}, choose a different bet"))
                    bets[player_index] = bet
                    if sum(bets) != self.round:
                        break

        for player, bet in zip(self.players, bets):
            player.bet = bet

    def update_scores(self):
        for player in self.players:
            player.score += abs(player.bet - player.tricks_won)

    def play_trick(self, starting_player_index):

        played = []
        for i in range(4):
            player_index = (starting_player_index + i) % 4
            player = self.players[player_index]

            card = player.hand.pop(0)
            played.append((player, card))
            print(f"{player.name} plays {card}")

        winner = max(played, key=lambda x: card_rank(x[1]))[0]
        winner.tricks_won += 1
        print(f"{winner.name} wins the trick")
        return winner

    def determine_winners(self):
        pass

    def handle_ties(self):
        pass

    def eliminate_players(self):
        pass

    def game_over(self):
        pass
