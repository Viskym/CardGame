import unittest
from FiveCardDraw import *


class TestFiveCardDraw(unittest.TestCase):
    def setUp(self):
        """Set up a game instance with known player names and a fixed starting money amount."""
        self.game = FiveCardDraw(['Alice', 'Bob'], 100)
        self.RoyalFlush = [Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K'),
                           Card('Hearts', 'A')]
        self.StraightFlush =[Card('Hearts', '9'), Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K')]
        self.Four = [Card('Clubs', '5'), Card('Hearts', '5'), Card('Diamonds', '5'), Card('Spades', '5'),
                     Card('Hearts', 'A')]
        self.FullHouse = [Card('Clubs', '3'), Card('Diamonds', '3'), Card('Hearts', '3'), Card('Hearts', '6'),
                          Card('Diamonds', '6')]
        self.Flush = [Card('Hearts', '2'), Card('Hearts', '4'), Card('Hearts', '6'), Card('Hearts', '8'),
                      Card('Hearts', 'J')]
        self.Strait = [Card('Clubs', '5'), Card('Diamonds', '6'), Card('Hearts', '7'), Card('Spades', '8'),
                       Card('Hearts', '9')]
        self.Three = [Card('Clubs', '7'), Card('Diamonds', '7'), Card('Hearts', '7'), Card('Hearts', '4'),
                      Card('Diamonds', '2')]
        self.TwoPair = [Card('Clubs', '4'), Card('Diamonds', '4'), Card('Hearts', '9'), Card('Spades', '9'),
                        Card('Hearts', '2')]
        self.APair = [Card('Clubs', '4'), Card('Diamonds', '2'), Card('Hearts', '5'), Card('Spades', '5'),
                      Card('Hearts', 'K')]
        self.HighCard = [Card('Clubs', '3'), Card('Clubs', '4'), Card('Clubs', '2'), Card('Hearts', '6'),
                         Card('Hearts', 'K')]

    def test_cards(self):
        self.cardA = Card('Hearts', 'A')
        self.card10 = Card('Clubs', '10')
        temp = Card('Hearts', 'A') > Card('Clubs', '10')
        self.assertEqual(temp, True)

    def test_hand_rank(self):
        # Royal Flush
        self.assertEqual(hand_rank(self.RoyalFlush), (8, 'A'))

        # Straight Flush
        self.assertEqual(hand_rank(self.StraightFlush), (8, 'K'))

        # Four of a Kind
        self.assertEqual(hand_rank(self.Four), (7, ['5', 'A']))

        # Full House
        self.assertEqual(hand_rank(self.FullHouse), (6, ['3', '6']))

        # Flush
        self.assertEqual(hand_rank(self.Flush), (5, ['J', '8', '6', '4', '2']))

        # Straight
        self.assertEqual(hand_rank(self.Strait), (4, '9'))

        # Three of a Kind
        self.assertEqual(hand_rank(self.Three), (3, ['7', '4', '2']))

        # Two Pair
        self.assertEqual(hand_rank(self.TwoPair), (2, ['9', '4', '2']))

        # A Pair
        self.assertEqual(hand_rank(self.APair), (1, ['5', 'K', '4', '2']))

        # High Card
        self.assertEqual(hand_rank(self.HighCard), (0, ['K', '6', '4', '3', '2']))

    def test_compare_hands(self):
        P1 = Player('Alice')
        P2 = Player('Bob')

        P1.hands = self.RoyalFlush
        P2.hands = self.StraightFlush
        self.assertEqual(compare_hands(P1,P2), P1)

        P1.hands = self.TwoPair
        P2.hands = self.FullHouse
        self.assertEqual(compare_hands(P1, P2), P1)


# This allows the tests to be run from the command line
if __name__ == '__main__':
    unittest.main()
