from cards import Card, create_card_list
from collections import Counter
import functools


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return inner


@memoize
def hand_rank(hand):
    """
    Determines the ranking of a poker hand. Disable @memoize for doctests.

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

    # Efficient rank and suit extraction
    ranks = [card.rank for card in hand]
    suits = [card.suit for card in hand]

    # Count the occurrences of each rank
    rank_counts = Counter(ranks)
    sorted_ranks = sorted(rank_counts, key=lambda r: (-rank_counts[r], -Card.ranks.index(r)))

    flush = len(set(suits)) == 1
    rank_indices = sorted(Card.ranks.index(rank) for rank in ranks)
    straight = len(set(rank_indices)) == 5 and (rank_indices[-1] - rank_indices[0] == 4)

    if straight and flush:
        return (8, Card.ranks[rank_indices[-1]])  # Straight flush
    if rank_counts[sorted_ranks[0]] == 4:
        return (7, [sorted_ranks[0], sorted_ranks[-1]])  # Four of a kind
    if rank_counts[sorted_ranks[0]] == 3 and rank_counts[sorted_ranks[1]] == 2:
        return (6, sorted_ranks[:2])  # Full house
    if flush:
        return (5, sorted_ranks)  # Flush
    if straight:
        return (4, Card.ranks[rank_indices[-1]])  # Straight
    if rank_counts[sorted_ranks[0]] == 3:
        return (3, sorted_ranks[:3])  # Three of a kind
    if list(rank_counts.values()).count(2) == 2:
        return (2, sorted_ranks[:2])  # Two pairs
    if 2 in rank_counts.values():
        return (1, sorted_ranks[:2])  # One pair
    return (0, sorted_ranks)  # High card


if __name__ == '__main__':
    import time

    t = time.perf_counter()
    case2 = create_card_list("[♠10, ♣2, ♥K, ♣8, ♦5]")
    print(hand_rank(case2))
    elapsed_time = time.perf_counter() - t
    print(elapsed_time)
