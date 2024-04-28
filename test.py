import unittest

import cards
from FiveCardDraw import *
from unittest.mock import patch
from bot import *

class TestFiveCardDraw(unittest.TestCase):
    def setUp(self):
        """Set up a game instance with known player names and a fixed starting money amount."""
        self.game = FiveCardDraw(['Alice', 'Bob'], 100)
        self.RoyalFlush = [Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K'),
                           Card('Hearts', 'A')]
        self.StraightFlush = [Card('Hearts', '9'), Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'),
                              Card('Hearts', 'K')]
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
        self.hand1 = cards.create_card_list("[♥10, ♣Q, ♣3, ♠4, ♥5]")
        self.hand2 = cards.create_card_list("[♠10, ♣2, ♥K, ♣8, ♦5]")

    def test_cards(self):
        self.cardA = Card('♥', 'A')
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

        # Cases from games
        self.assertEqual(hand_rank(self.hand1), (0, ['Q', '10', '5', '4', '3']))
        self.assertEqual(hand_rank(self.hand2), (0, ['K', '10', '8', '5', '2']))

    def test_compare_hands(self):
        P1 = Player('Alice')
        P2 = Player('Bob')

        P1.hands = self.RoyalFlush
        P2.hands = self.StraightFlush
        self.assertEqual(compare_hands(P1, P2), P1)

        P1.hands = self.TwoPair
        P2.hands = self.FullHouse
        self.assertEqual(compare_hands(P1, P2), P1)

        P1.hands = self.hand1
        P2.hands = self.hand2
        self.assertEqual(compare_hands(P1, P2), P2)

        P1.hands = cards.create_card_list("[♥4, ♥Q, ♠2, ♥5, ♠A]")
        P2.hands = cards.create_card_list("[♦2, ♦3, ♦4, ♥7, ♥A]")
        self.assertEqual(compare_hands(P1, P2), P1)
    @patch('builtins.input', side_effect=['bet', '10', 'fold'])
    @patch('builtins.print')
    def test_betting_round(self, mock_print, mock_input):
        """
        Test betting round where Alice bets 10 and Bob folds.
        """
        self.game.betting_round()

        # Assert Alice's money is reduced by 10 and Bob is inactive
        self.assertEqual(self.game.players[0].money, 90)  # Alice starts with 100 and bets 10
        self.assertFalse(self.game.players[1].active)  # Bob folds
        self.assertEqual(self.game.pot, 10)  # Pot should have Alice's bet

    @patch('builtins.input', side_effect=['check', 'check'])
    @patch('builtins.print')
    def test_betting_round_checks(self, mock_print, mock_input):
        """
        Test betting round where both players check.
        """
        self.game.betting_round()

        # Assert that no money is taken and both are still active
        self.assertEqual(self.game.players[0].money, 100)  # Alice's money remains the same
        self.assertEqual(self.game.players[1].money, 100)  # Bob's money remains the same
        self.assertTrue(self.game.players[0].active)  # Alice is still active
        self.assertTrue(self.game.players[1].active)  # Bob is still active
        self.assertEqual(self.game.pot, 0)  # Pot should remain empty

    def test_pattern(self):
        self.assertEqual(choose_discard("PatternKeeper",self.RoyalFlush), [])

        # Straight Flush
        self.assertEqual(choose_discard("PatternKeeper",self.StraightFlush), [])

        # Four of a Kind
        self.assertEqual(choose_discard("PatternKeeper",self.Four), [5])

        # Full House
        self.assertEqual(choose_discard("PatternKeeper",self.FullHouse), [])

        # Flush
        self.assertEqual(choose_discard("PatternKeeper",self.Flush), [])
        #
        # # Straight
        self.assertEqual(choose_discard("PatternKeeper",self.Strait), [])
        #
        # # Three of a Kind
        self.assertEqual(choose_discard("PatternKeeper",self.Three), [4,5])

        # # Two Pair
        self.assertEqual(choose_discard("PatternKeeper",self.TwoPair), [5])
        #
        # # A Pair
        self.assertEqual(choose_discard("PatternKeeper",self.APair), [1,2,5])
        #
        # # High Card
        self.assertEqual(choose_discard("PatternKeeper",self.HighCard), [1,2,3,4])
        #
        # # Cases from games
        self.assertEqual(choose_discard("PatternKeeper",self.hand1), [1,3,4,5])
        self.assertEqual(choose_discard("PatternKeeper",self.hand2), [1,2,4,5])

# This allows the tests to be run from the command line
if __name__ == '__main__':
    unittest.main()
