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

        self.players = [Player(name) for name in player_names]
        self.round = 1
        self.dealer_index = 0
        self.state = 'betting'
        self.bets = [None]*4
        self.played_cards = []
        self.current_trick = []
        self.current_player_index = (self.dealer_index +1)%4
        self.next_round_double = False
        self.deck = None


    def start_new_round(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_cards()

        for player in self.players:
            player.tricks_won = 0

        self.bets = [None]*4
        self.played_cards = []
        self.current_trick = []
        self.current_player_index = (self.dealer_index +1)%4


    def deal_cards(self):
        for player in self.players:
            player.hand = []
            for _ in range(self.round):
                card = self.deck.draw()
                if card:
                    player.hand.append(card)


    def set_bet(self, player_index, bet):
        #return true if bet is valid
        self.bets[player_index] = bet
        self.players[player_index].bet = bet
        if player_index == (self.dealer_index +3)%4:
            if sum(self.bets) == self.round:
                self.bets[player_index] = None
                self.players[player_index].bet = None
                return False
            else:
                self.state = 'playing'

        #advance to next player
        self.current_player_index = (self.current_player_index +1)%4
        if all(b is not None for b in self.bets):
            self.state = 'playing'
            self.current_player_index = (self.dealer_index +1)%4
        return True


    def get_player_hand(self, player_index):
        return self.players[player_index].hand


    def get_scores(self):
        return [p.score for p in self.players]


    def get_current_player(self):
        return self.current_player_index


    def get_state(self):
        return self.state


    def play_card(self, player_index, card_index):
        #return winner_index and trick_end if end, else none
        if self.state != 'playing':
            return None

        card = self.players[player_index].hand.pop(card_index)
        self.current_trick.append((player_index, card))
        if len(self.current_trick) == 4:
            winner_index = self.resolve_trick()
            self.current_trick = []
            self.played_cards.append([c for _, c in self.current_trick])
            #check if round ends
            if all(len(p.hand) == 0 for p in self.players):
                self.update_scores()
                self.state = 'round_end'
            self.current_player_index = winner_index
            return (winner_index, True)
        else:
            self.current_player_index = (self.current_player_index +1)%4
            return (None, False)


    def resolve_trick(self):
        played = [(self.players[i], c) for i, c in self.current_trick]
        #special cards and voided logic
        special_cards = {(7, 'Diamonds'), (7, 'Spades'), (14, 'Clubs'), (14, 'Spades')}
        value_counts = {}
        for _, card in played:
            if (card.value, card.suit) not in special_cards:
                value_counts[card.value] = value_counts.get(card.value, 0) +1
        if len(set(card.value for _, card in played)) == 1:
            self.next_round_double = True
            return None
        voided_values = {v for v, count in value_counts.items() if count>1}
        valid_plays = [(player, card) for player, card in played if card.value not in voided_values or (card.value, card.suit) in special_cards]
        if not valid_plays:
            return None
        winner = max(played, key=lambda x: card_rank(x[1]))[0]
        winner.tricks_won +=1
        return self.players.index(winner)


    def update_scores(self):
        for player in self.players:
            player.score += abs(player.bet - player.tricks_won)


    def next_round(self):
        self.round += 1
        self.dealer_index = (self.dealer_index +1)%4
        self.start_new_round()


    def is_game_over(self):
        return self.round >9


    def get_visible_cards(self, player_index):
        if self.round == 1:
            return {i: self.players[i].hand[0] for i in range(4) if i != player_index}
        else:
            return {player_index: self.players[player_index].hand}