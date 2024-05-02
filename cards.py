import random


class Card:
    """
    Represents a playing card with a suit and rank.

    >>> cardA = Card('Hearts', 'A')
    >>> card10 = Card('Clubs', '10')
    >>> cardA > card10
    True
    >>> print(card10)
    """
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']

    def __init__(self, suit, rank) -> None:
        self.suit_dict = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
        if suit in self.suit_dict.keys():
            self.suit = self.suit_dict[suit]
        else:
            self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return self.suit + self.rank

    def __str__(self) -> str:
        color_dict = {
            '♠': '\033[30m♠\033[0m',
            '♥': '\033[31m♥\033[0m',
            '♦': '\033[31m♦\033[0m',
            '♣': '\033[30m♣\033[0m',
        }
        return color_dict[self.suit] + self.rank

    def reveal(self):
        print(str(self))
        return str(self)

    def __eq__(self, other):
        return (self.ranks.index(self.rank), self.suits.index(self.suit)) == (
            self.ranks.index(other.rank), self.suits.index(other.suit))

    def __lt__(self, other):
        return (self.ranks.index(self.rank), self.suits.index(self.suit)) < (
            self.ranks.index(other.rank), self.suits.index(other.suit))

    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    def __init__(self) -> None:
        self.__suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.__values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = []
        for s in self.__suits:
            for v in self.__values:
                self.cards.append(Card(s, v))
        random.shuffle(self.cards)

    def __str__(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        """
        Pops out the last item.
        """
        if not self.cards:
            print("The deck is empty.")
        else:
            drawcard = self.cards.pop()
            return drawcard

    def reset(self):
        self.__init__()

    def sort_by_suit(self):
        self.cards.sort()

    def sort_by_value(self):
        def card_sort_key(card):
            return (self.__values.index(card.rank), self.__suits.index(card.suit))

        self.cards = sorted(self.cards, key=card_sort_key)

    def remove(self, card: Card):
        self.cards.remove(card)


class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.wins = 0
        self.hands = []
        self.money = 0

    def draw(self, deck):
        self.hands.append(deck.draw())
        return self.hands[-1]

    def clearHand(self):
        self.hands.clear()

    def __str__(self) -> str:
        return f"{self.name}:{self.hands}"

    def __lt__(self, other):
        return self.wins < other.wins

    def __eq__(self, other):
        return self.wins == other.wins


def create_card_list(card_string):
    import re
    # Extract cards from the string using a pattern that captures suit symbols followed by one or more digits or letters
    card_pattern = r'([♥♦♣♠])(\d{1,2}|[JQKA])'
    matches = re.findall(card_pattern, card_string)

    cards = []
    for suit, rank in matches:
        cards.append(Card(suit, rank))

    return cards
