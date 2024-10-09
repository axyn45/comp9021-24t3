import random

# Constants for suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# A function to generate a shuffled deck based on a given seed
def shuffle_deck(deck:list,seed):
    deck.sort()
    print(deck)
    # deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.seed(seed)
    random.shuffle(deck)
    print(deck)
    return deck

# A function to check if a card can be placed on an increasing sequence (based on Ace)
def can_place_on_increasing(card, stack):
    rank, suit = card
    if(rank=='K'):return False
    if not stack:
        return rank == 'A'
    last_rank, last_suit = stack[-1]
    return suit == last_suit and RANKS.index(rank) == RANKS.index(last_rank) + 1

# A function to check if a card can be placed on a decreasing sequence (based on King)
def can_place_on_decreasing(card, stack):
    rank, suit = card
    if not stack:
        return rank == 'K'
    last_rank, last_suit = stack[-1]
    return suit == last_suit and RANKS.index(rank) == RANKS.index(last_rank) - 1

# Function to run a single game
def play_game(seed):
    roundcount=0
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    deck = shuffle_deck(deck,seed)
    increasing_stacks = {suit: [] for suit in SUITS}
    decreasing_stacks = {suit: [] for suit in SUITS}
    # unplaced_cards = []
    cards_to_place = []

    while True:
        placed_count=0
        while len(deck):
            # new_cards = []
            # Draw the top 3 cards from the deck, if possible
            for _ in range(min(3, len(deck))):
                cards_to_place.append(deck.pop())
            # print(cards_to_place)

            # Try to place cards on stacks
            for card in reversed(cards_to_place):
                rank, suit = card
                if can_place_on_increasing(card, increasing_stacks[suit]):
                    increasing_stacks[suit].append(card)
                    placed_count=placed_count+1
                    del cards_to_place[-1]
                    # print('----------------------------------------------------')
                    # for i in increasing_stacks:
                    #     print(i)
                    #     for j in range(len(increasing_stacks[i])):
                    #         print(increasing_stacks[i][j][0],end=' ')
                    #     print()
                    #     for j in range(len(decreasing_stacks[i])):
                    #         print(decreasing_stacks[i][j][0],end=' ')
                    #     print('\n')
                elif can_place_on_decreasing(card, decreasing_stacks[suit]):
                    decreasing_stacks[suit].append(card)
                    placed_count=placed_count+1
                    del cards_to_place[-1]
                    # print('----------------------------------------------------')
                    # for i in increasing_stacks:
                    #     print(i)
                    #     for j in range(len(increasing_stacks[i])):
                    #         print(increasing_stacks[i][j][0],end=' ')
                    #     print()
                    #     for j in range(len(decreasing_stacks[i])):
                    #         print(decreasing_stacks[i][j][0],end=' ')
                    #     print('\n')
                else:
                    break
        roundcount=roundcount+1
        if(placed_count==0):
            break
        deck=cards_to_place
        # shuffle_deck(deck,seed+roundcount)
        cards_to_place=[]
        # print(placed_count)
        # print(deck)
        # print(roundcount)
        placed_count=0

    for i in increasing_stacks:
        print(i)
        for j in range(len(increasing_stacks[i])):
            print(increasing_stacks[i][j][0],end=' ')
        print()
        for j in range(len(decreasing_stacks[i])):
            print(decreasing_stacks[i][j][0],end=' ')
        print('\n')

    if not len(cards_to_place):
        print("All cards have been placed, you won!")
    else:
        print(f"{len(cards_to_place)} cards could not be placed, you lost!")
    
    # Display output for user interaction
    collected_output = []
    collected_output.append("Deck shuffled, ready to start!")
    collected_output.append(f"{'[]' * len(deck)}")
    for suit in SUITS:
        increasing = ''.join(['[]' if len(increasing_stacks[suit]) == 0 else str(increasing_stacks[suit][-1])])
        decreasing = ''.join(['[]' if len(decreasing_stacks[suit]) == 0 else str(decreasing_stacks[suit][-1])])
        collected_output.append(f"Increasing for {suit}: {increasing}")
        collected_output.append(f"Decreasing for {suit}: {decreasing}")
    
    return collected_output

# Main function to run the game
def main(seedparam=None):
    if(not seedparam==None):seed_value=int(seedparam)
    else:seed_value = int(input("Please enter an integer to feed the seed() function: "))
    output = play_game(seed_value)
    
    # Handle user interaction for displaying parts of the output
    while True:
        print(f"There are {len(output)} lines of output; what do you want me to do?")
        print("Enter: q to quit")
        print("a last line number (between 1 and _)")
        print("a first line number (between -1 and -_)")
        print("a range of line numbers (of the form m--n with 1 <= m <= n <= _)")

        user_input = input().strip()
        if user_input == 'q':
            break
        elif user_input.isdigit() and 1 <= int(user_input) <= len(output):
            print('\n'.join(output[:int(user_input)]))
        elif user_input.startswith('-') and user_input[1:].isdigit() and 1 <= int(user_input[1:]) <= len(output):
            print('\n'.join(output[-int(user_input):]))
        elif '--' in user_input:
            m, n = map(int, user_input.split('--'))
            if 1 <= m <= n <= len(output):
                print('\n'.join(output[m-1:n]))
        else:
            print("Invalid input")

if __name__ == "__main__":
    main(8)
