from cards import *
import bot

class FiveCardDraw:
    def __init__(self, player_names, starting_money):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        for player in self.players:
            player.money = starting_money
            player.active = True
        self.pot = 0

    def deal_cards(self):
        self.deck.shuffle()
        for player in self.players:
            player.hands = [self.deck.draw() for _ in range(5)]

    def show_hands(self):
        for player in self.players:
            print(f"{player.name}'s hand: {player.hands}")

    def betting_round(self):
        """
        Start Betting Round:
        Begin with the first player.
        Is Player Active?:
        Check if the player is currently active (i.e., not folded in previous betting rounds).
        If No, skip to the next player.
        If Yes, proceed to the next step.
        Has a Bet Been Made?:
        Determine if there has been a bet in this round.
        If No, the player has three options: Bet, Check, or Fold.
        If Yes, the player has three options: Call, Raise, or Fold.
        Player Decision (No Previous Bet):
        Bet: The player decides to bet. Prompt for bet amount, subtract from player's money, add to pot, and set this as the current bet.
        Check: The player decides to check, do nothing.
        Fold: The player decides to fold, mark player as inactive.
        Player Decision (With Previous Bet):
        Call: The player meets the current bet. Subtract the bet amount from player's money, add to pot.
        Raise: The player increases the bet. Prompt for new total bet amount, check if it's greater than the current bet, subtract from player's money, add to pot, update the current bet.
        Fold: The player decides to fold, mark player as inactive.
        Next Player:
        Move to the next player and repeat the process.
        End of Round Check:
        After all players have made their decisions, check if additional responses are needed (e.g., if there was a raise).
        If additional betting is required (e.g., due to a raise), repeat the betting round starting from the next player after the one who made the raise.
        If no further betting is required, conclude the betting round.
        End Betting Round:
        The betting round ends when all active players have either called the highest bet or folded.
        """
        current_bet = 0
        num_bets = 0  # Tracks number of bets to handle raises correctly

        for player in self.players:
            if not player.active:
                continue

            while True:
                if current_bet == 0:
                    action = input(f"{player.name}, do you want to bet, fold, or check? (bet/fold/check): ")
                    if action == 'fold':
                        player.active = False
                        break
                    elif action == 'bet':
                        bet_amount = int(input(f"{player.name}, how much would you like to bet? "))
                        if bet_amount <= 0 or bet_amount > player.money:
                            print("Invalid bet amount.")
                            continue
                        player.money -= bet_amount
                        self.pot += bet_amount
                        current_bet = bet_amount
                        num_bets += 1
                        break
                    elif action == 'check':
                        break
                else:
                    action = input(f"{player.name}, do you want to call, raise, or fold? (call/raise/fold): ")
                    if action == 'fold':
                        player.active = False
                        break
                    elif action == 'call':
                        if player.money < current_bet:
                            print(f"Not enough funds to call. {player.name} folds.")
                            player.active = False
                        else:
                            player.money -= current_bet
                            self.pot += current_bet
                        break
                    elif action == 'raise':
                        raise_amount = int(input(f"{player.name}, how much total would you like to bet? "))
                        if raise_amount <= current_bet or raise_amount > player.money:
                            print("Invalid raise amount.")
                            continue
                        player.money -= raise_amount
                        self.pot += raise_amount
                        current_bet = raise_amount
                        num_bets += 1
                        break

        # Allow other players to respond to the last bet/raise
        if num_bets > 1:
            self.betting_round()

    def draw_phase(self):
        for player in self.players:
            if player.name == 'Bob':
                discard_indices = bot.choose_discard("PatternKeeper", player.hands)
                print(f"Bob discarded: {discard_indices}")
                self.replace_cards(player, discard_indices)
            else:
                if not player.active:
                    continue
                print(f"{player.name}'s current hand: {player.hands}")
                discard_indices = input("Enter the positions of cards to discard (e.g., 1 3 5): ")
                discard_indices = list(map(int, discard_indices.split()))
                self.replace_cards(player, discard_indices)

    def replace_cards(self, player, discard_indices):
        for index in sorted(discard_indices, reverse=True):
            player.hands.pop(index - 1)  # Adjusting index for 0-based indexing
        for _ in range(len(discard_indices)):
            player.hands.append(self.deck.draw())

    def determine_winner(self):
        best_player = None
        for player in self.players:
            if not player.active:
                continue
            if not best_player:
                best_player = player
            else:
                best_player = compare_hands(best_player, player)
        return best_player


def hand_rank(hand):
    """
    Determines the ranking of a poker hand.

    >>> RoyalFlush = [Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K'), Card('Hearts', 'A')]
    >>> hand_rank(RoyalFlush)
    (8, 'A')

    >>> StraightFlush = [Card('Hearts', '9'), Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K')]
    >>> hand_rank(StraightFlush)
    (8, 'K')

    >>> Four = [Card('Clubs', '5'), Card('Hearts', '5'), Card('Diamonds', '5'), Card('Spades', '5'), Card('Hearts', 'A')]
    >>> hand_rank(Four)
    (7, ['5', 'A'])

    >>> case2 = create_card_list("[♠10, ♣2, ♥K, ♣8, ♦5]")
    >>> hand_rank(case2)
    (0, ['K', '10', '8', '5', '2'])
    """
    hand_only_rank = [c.rank for c in hand]
    rank_counts = {r: ''.join(sorted(hand_only_rank)).count(r) for r in hand_only_rank}
    rank_sorted = sorted(rank_counts, key=lambda r: (rank_counts[r], Card.ranks.index(r)), reverse=True)
    rank_sorted_by_index = sorted(rank_sorted, key=lambda r: Card.ranks.index(r), reverse=True)

    flush = len(set(card.suit for card in hand)) == 1
    straight = Card.ranks.index(rank_sorted_by_index[0]) - Card.ranks.index(rank_sorted_by_index[-1]) == 4 and len(set(rank_sorted_by_index)) == 5

    if straight and flush:
        return (8, rank_sorted_by_index[0])  # Straight flush
    elif rank_counts[max(rank_sorted, key=rank_counts.get)] == 4:
        return (7, rank_sorted)  # Four of a kind
    elif sorted(rank_counts.values()) == [2, 3]:
        return (6, rank_sorted)  # Full house
    elif flush:
        return (5, rank_sorted)  # Flush
    elif straight:
        return (4, rank_sorted_by_index[0])  # Straight
    elif rank_counts[max(rank_sorted, key=rank_counts.get)] == 3:
        return (3, rank_sorted)  # Three of a kind
    elif list(rank_counts.values()).count(2) == 2:
        return (2, rank_sorted)  # Two pairs
    elif 2 in rank_counts.values():
        return (1, rank_sorted)  # One pair
    else:
        return (0, rank_sorted_by_index)  # High card


def compare_hands(player1, player2):
    hand1, hand2 = player1.hands, player2.hands
    rank1, rank2 = hand_rank(hand1), hand_rank(hand2)
    # Printing the hands and their ranks for comparison
    hand_types = ["High card", "One pair", "Two pairs", "Three of a kind", "Straight", "Flush", "Full house",
                  "Four of a kind", "Straight flush"]
    print(f"{player1.name} has a {hand_types[rank1[0]]} ({rank1[1]}) with {hand1}")
    print(f"{player2.name} has a {hand_types[rank2[0]]} ({rank2[1]}) with {hand2}")

    if rank1[0] == rank2[0]:  # If the type of hand is the same
        for card1, card2 in zip(rank1[1], rank2[1]):  # Compare each card
            if Card.ranks.index(card1) > Card.ranks.index(card2):
                return player1
            elif Card.ranks.index(card1) < Card.ranks.index(card2):
                return player2
        return None  # All cards match, it's a tie
    elif rank1 > rank2:
        return player1
    else:
        return player2


# Modify the determine_winner function to use this
def determine_winner(self):
    best_player = None
    for player in self.players:
        if not player.active:
            continue
        if not best_player:
            best_player = player
        else:
            best_player = compare_hands(best_player, player)
    return best_player


if __name__ == '__main__':
    # Example game setup
    game = FiveCardDraw(['Alice', 'Bob'], 100)
    game.deal_cards()
    game.show_hands()
    game.betting_round()
    game.draw_phase()
    game.show_hands()
    game.betting_round()
    winner = game.determine_winner()
    print(f"The winner is {winner.name} with the hand {winner.hands}")
