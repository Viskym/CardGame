from cards import *
#from FiveCardDraw import hand_rank

def choose_betting(isFinal: bool, hand: list[Card]):
    """
    >>> choose_betting(False,cards.create_card_list("[♥4, ♥Q, ♠2, ♥5, ♠A]"))
    ('check',0)
    >>> choose_betting(True,cards.create_card_list("[♥4, ♥Q, ♠2, ♥5, ♠A]"))
    ('call',0)
    >>> chooose_betting(False,cards.create_card_list("[♠5, ♥5, ♠4, ♣8, ♥8]"))
    ('raise',0.25)
    >>> chooose_betting(True,cards.create_card_list("[♠5, ♥5, ♠4, ♣8, ♥8]"))
    ('call',0)
    >>> chooose_betting(True,cards.create_card_list("[♦5, ♥Q, ♠9, ♦9, ♥9]"))
    ('raise',0.25)
    """
    return ('call',0)


def choose_discard(mode: str, hand: list[Card]):
    """
    PatternKeeper:
    1. Evaluate existing hand
    2. keep the highest formed pattern. Discard the rest.
    pro: works for pair, two pairs, three of a kind, four of a kind
    con: Unable to form strategy for flush,straight. It will see straight and flush candidates as Highcard.


    >>> choose_discard("PatternKeeper",create_card_list("[♥4, ♥Q, ♠2, ♥5, ♠A]"))
    [1, 2, 3, 4]
    >>> choose_discard("PatternKeeper",create_card_list("[♣4, ♦4, ♥10, ♦A, ♣Q]"))
    [3, 4, 5]
    >>> choose_discard("PatternKeeper",create_card_list("[♠5, ♥5, ♠4, ♣8, ♥8]"))
    [3]
    >>> choose_discard("PatternKeeper",create_card_list("[♠4, ♦5, ♠6, ♣4, ♥4]"))
    [2, 3]
    >>> choose_discard("DecisionTree",create_card_list("[♣A, ♣4, ♣8, ♣5, ♥7]"))
    [5]
    >>> choose_discard("DecisionTree",create_card_list("[♦9, ♦10, ♥6, ♥Q, ♠8]"))
    [2]
    """
    #hand_types = ["High card", "One pair", "Two pairs", "Three of a kind", "Straight", "Flush", "Full house",
                  # "Four of a kind", "Straight flush"]

    match mode:
        case 'PatternKeeper':
            pattern,rank_sorted  = hand_rank(hand)
            discard_list = []
            hand_only_rank = [c.rank for c in hand]
            rank_sorted_by_index = sorted(rank_sorted, key=lambda r: Card.ranks.index(r), reverse=True)
            match pattern:
                case 8:
                    pass
                case 7: #four of a kind
                    discard_list.append(hand_only_rank.index(rank_sorted[1])+1)
                case 6: #full house
                    pass
                case 5: #flush
                    pass
                case 4: #straight
                    pass
                case 3: #three of a kind
                    discard_list.append(hand_only_rank.index(rank_sorted[1])+1)
                    discard_list.append(hand_only_rank.index(rank_sorted[2])+1)
                case 2: #two pairs
                    discard_list.append(hand_only_rank.index(rank_sorted[-1])+1)
                case 1: #one pair
                    for i in range(1,4):
                        discard_list.append(hand_only_rank.index(rank_sorted[i])+1)
                case 0: #high card
                    for i in range(1,5):
                        discard_list.append(hand_only_rank.index(rank_sorted_by_index[i])+1)

    #generate discard
        case 'DecisionTree':
            pass
    return sorted(discard_list) if len(discard_list) != 0 else discard_list


def best_discard_strategy(hand):
    # Initialize variables to track the best strategy and its value
    max_value = 0
    best_discard = []

    # Evaluate all possible discard combinations
    for discard_set in generate_all_possible_discards(hand):
        # Simulate the outcome of drawing new cards for each discard
        for new_hand in simulate_new_hands(hand, discard_set):
            # Calculate the value of the new hand
            hand_value = evaluate_hand(new_hand)
            
            # Update the best discard strategy if this hand is better
            if hand_value > max_value:
                max_value = hand_value
                best_discard = discard_set

    return best_discard

def generate_all_possible_discards(hand):
    discards = [[]]

    for card in hand: 
        subsets_to_add = [] # Initialises a subset list as empty, that will be added to discards

        for subset in discards: 
            # For each subset currently in discards, add the current card, append these to discards
            new_subset = subset + [card]
            subsets_to_add.append(new_subset)
            print("Card is: ", card, "adding to create: ", new_subset)
        discards.extend(subsets_to_add)
    return discards[1:] # Do not return initial empty list

print(len(generate_all_possible_discards([1, 2, 3, 4, 5])))



"""
function simulate_new_hands(original_hand, discard_set):
    # Simulate drawing cards to replace the discarded ones and generate new hands. 
    remaining_deck = get_remaining_deck(original_hand, discard_set)
    return generate_new_hands(original_hand, discard_set, remaining_deck)

function evaluate_hand(hand):
    # Determine the poker value of a hand based on poker rules
    return calculate_hand_value(hand)

function get_remaining_deck(hand, discarded):
    # Determine which cards are left in the deck after discards
    return remove_discarded_from_deck(hand, discarded)

function generate_new_hands(hand, discarded, deck):
    # Form new hands by combining remaining hand cards with new draws from the deck
    remaining_hand = remove_cards(hand, discarded)
    possible_draws = get_combinations(deck, len(discarded))
    return [combine(remaining_hand, draw) for draw in possible_draws]
"""
