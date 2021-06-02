import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def deal_card(self):
        single_card = self.deck.pop()
        return single_card
    
    def __str__(self):
        all_cards = ''
        for i in self.deck:
            all_cards += str(i) + '\n'
        return all_cards

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.ace += 1

    def adjust_ace(self):
        if self.value > 21 and self.ace:
            self.value -= 10
            self.ace -= 1

    def __str__(self):
        l = ''
        for i in self.cards:
            l += str(i) + '\n'
        return l

class Chips():
    def __init__(self):
        self.ammount = 100
        self.bet = 0
        
    def win(self):
        self.ammount += self.bet

    def lose(self):
        self.ammount -= self.bet

play_deck = Deck()
dealer = Hand()
hide = Hand()
player = Hand()
player_chips = Chips()

def pull_card():
    pulled = play_deck.deal_card()
    return pulled

def hit_stand():
    move = input('Do you want to hit or stand h/s: ')
    if move == 'h':
        return True
    else:
        return False

def dist_cards():
    dealer.add_card(pull_card())
    player.add_card(pull_card())

def dist_cards_player():
    hit = hit_stand()
    if hit == True:
        player.add_card(pull_card())

def hide_dealer():
    hide.__init__()
    for i in range(len(dealer.cards)):
        hide.cards.append(dealer.cards[i])
    hide.value = dealer.value
    hide.value -= values[dealer.cards[0].rank]
    hide.cards.pop(0)

def print_some():
    hide_dealer()
    print(f'\n Dealer Cards: \n<hidden card>\n{hide}\t{hide.value}')
    print(f'\n Player Cards: \n{player}\t{player.value}\n\n')

def print_all():
    print(f'\nSHOWDOWN\n\n Dealer Cards: \n{dealer}\t{dealer.value}\n\n')

def close_to_21():
    if (21 - dealer.value) > (21 - player.value) and player.value <= 21:
        return 'player'
    elif dealer.value <= 21:
        return 'dealer'

def rounds():
    showdown = 0
    while True:
        if showdown == 0:
            dist_cards()
            dist_cards()
            print_some()
        if player.value == 21:
            return 'blackjack'        
        dist_cards_player()
        if showdown == 0:
            dealer.add_card(pull_card())
        if player.value > 21:
            player.adjust_ace()
            if player.value > 21:
                print_some()
                return 'player_bust'
        print_some()
        if hide.value > 21:
            hide.adjust_ace()
            if hide.value > 21:
                return  'dealer_bust'
        if showdown > 0 or hide.value >= 17:
            if dealer.value > 21:
                dealer.adjust_ace()
                if dealer.value > 21:
                    print_all()
                    return 'dealer_bust'
            else:
                print_all()
                return close_to_21()
        showdown += 1

def player_input_bet():
    while True:
        try:
            player_chips.bet = int(input('Enter your bet: '))
            if player_chips.bet > player_chips.ammount:
                print("You don't have enough money for that bet")
            else:
                break
        except:
            print('You must enter a number')

def money_calc(outcome):
    if outcome == 'dealer_bust' or outcome == 'player' or outcome == 'blackjack':
        player_chips.win()
    else:
        player_chips.lose()

def round_end(outcome):
    if outcome == 'dealer_bust':
        print(f'\n\nDealer Busted\n\nYou win: {player_chips.bet}\nYour current Balance: {player_chips.ammount}')
    elif outcome == 'player_bust':
        print(f'\n\nYou Busted\n\nYou lose: {player_chips.bet}\nYour current Balance: {player_chips.ammount}')
    if outcome == 'player':
        print(f'\n\nYou are closer to 21\n\nYou win: {player_chips.bet}\nYour current Balance: {player_chips.ammount}')
    elif outcome == 'dealer':
        print(f'\n\nDealer is closer to 21\n\nYou lose: {player_chips.bet}\nYour current Balance: {player_chips.ammount}')
    if outcome == 'blackjack':
        print(f'\n\nYou got Blackjack\n\nYou win: {player_chips.bet}\nYour current Balance: {player_chips.ammount}')

def quit(broke):
    if broke == True:
        quit = input('Do you want to play again y/n: ')
    else:
        quit = input('Do you want to play another hand y/n: ')
    print('\n\n')
    if quit == 'n':
        return False
    else:
        return True

def reset_hand():
    play_deck.__init__()
    play_deck.shuffle_deck()
    player.__init__()
    dealer.__init__()

playing = True
broke = False
player_chips.__init__()

print('\n\nWelcome to Blackjack\n\n')
while playing:
    print(f'You have: ${player_chips.ammount}')
    reset_hand()
    player_input_bet()
    outcome = rounds()
    money_calc(outcome)
    round_end(outcome)
    playing = quit(broke)
    if player_chips.ammount == 0 and playing == True:
        broke = True
        print('You are broke\n')
        playing = quit(broke)
        if playing == True:
            player_chips.__init__()
print('Thank You for playing')