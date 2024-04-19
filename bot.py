import cards


def choose_betting(isFinal: bool, hand: list[cards.Card]):
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
    pass


def choose_discard(mode: str, hand: list[cards.Card]):
    """
    PatternKeeper:
    1. Evaluate existing hand
    2. keep the highest formed pattern. Discard the rest.
    pro: works for pair, two pairs, three of a kind, four of a kind
    con: Unable to form strategy for flush,straight. It will see straight and flush candidates as Highcard.

    Highcard with A, discard the rest.
    >>> choose_discard("PatternKeeper",cards.create_card_list("[♥4, ♥Q, ♠2, ♥5, ♠A]"))
    [1,2,3,4]
    A pair, discard the rest.
    >>> choose_discard("PatternKeeper",cards.create_card_list("[♣4, ♦4, ♥10, ♦A, ♣Q]"))
    [3,4,5]
    Two pairs, discard the rest.
    >>> choose_discard("PatternKeeper",cards.create_card_list("[♠5, ♥5, ♠4, ♣8, ♥8]"))
    [3]
    Three of a kind, discard the rest.
    >>> choose_discard("PatternKeeper",cards.create_card_list("[♠4, ♦5, ♠6, ♣4, ♥4]"))
    [2,3]

    >>> choose_discard("DecisionTree",cards.create_card_list("[♣A, ♣4, ♣8, ♣5, ♥7]"))
    [5]
    >>> choose_discard("DecisionTree",cards.create_card_list("[♦9, ♦10, ♥6, ♥Q, ♠8]"))
    [2]
    """
    match mode:
        case 'PatternKeeper':
            pass
        case 'DecisionTree':
            pass
    return discard_list


"""
function best_discard_strategy(hand):
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

function generate_all_possible_discards(hand):
    # Generate all subsets of the hand (all possible sets of cards to discard), 32 in total.
    return generate_subsets(hand)

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
