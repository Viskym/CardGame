from cards import *

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

