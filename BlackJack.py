import random
from IPython.display import clear_output


game_win_score = 21

class Card():
    '''
        Class representing a card
    '''
    def __init__(self, suit, number):
        self.number = number
        self.suit = suit
        
    def value(self):
        if self.number > 10:
            return 10
        else:
            return self.number

    def __str__(self):
        val = str(self.number)
        if self.number == 1:
            val = 'Ace'
        elif self.number == 11:
            val = 'Jack'
        elif self.number == 12:
            val = 'Queen'
        elif self.number == 13:
            val = 'King'
        return 'Suit:{}, value:{}'.format(self.suit, val)
    
class Deck():
    '''
    Class representing a deck with its cards
    '''
    
    
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        return 'Deck size{}'.format(len(self.cards))
        
    def suffle(self):
        self.cards = []
        for suit in ['Spades', 'Diamonds', 'Clubs', 'Hearts']:
            for val in range(1,14):
                if val >10:
                    self.cards.append(Card(suit, 10))
                else:
                    self.cards.append(Card(suit, val))
        random.shuffle(self.cards)

    def give_me_card(self):
        card = self.cards.pop()
        return card

class Hand():
    
    def __init__(self):
        self.cards = []
        
    def has_finished(self):
        return self.compute_hand() < game_win_score
        
    def compute_hand(self):
        total = 0
        if self.cards.count == 0:
            pass
        else:
            for i in map(lambda card: card.value(), self.cards):
                total += i
        
        if self.has_aces():
            if total+10 < game_win_score:
                return total + 10
        return total
            
    def has_aces(self):
        for card in self.cards:
            if card.value == 1:
                return True
        return False
    
    def add_card(self, card):
        self.cards.append(card)
        
    def display(self):
        for card in self.cards:
            print(card)
        
class Player():
    '''
        Class representing the player
    '''
    def __init__(self, is_machine, money=0):
        self.is_machine = is_machine
        self.money = money
    
    def __str__(self):
        if(self.is_machine):
            return "Bank"
        else:
            return "Player, money:{}".format(self.money)
        
    def play(self, deck, player_score = 0):
        hand = Hand()
        if not self.is_machine:
            print('Player playing')
            while hand.compute_hand() < 17:
                hand.add_card(deck.give_me_card())

            print('Summary of player hand')
            hand.display()
            return hand.compute_hand()
        else:
            print('Bank playing')
            
            if hand.compute_hand() < player_score and hand.compute_hand() < game_win_score:
                while hand.compute_hand() < player_score and hand.compute_hand() < game_win_score:
                    hand.add_card(deck.give_me_card())
            
            print('Summary of bank hand')
            hand.display()
            return hand.compute_hand()

        
    def is_penniless(self):
        return self.money == 0
    
    def place_bet(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def game_won(self, amount):
        self.money += amount
        
class Game():
    
    bank = Player(True)
    
    def __init__(self, player):
        self.player = player
    
    def place_bet(self):
        is_accepted = False
        while not is_accepted:
            try: 
                bet = int(input('Please place your bet:'))
                is_accepted = player.place_bet(bet)
                if not is_accepted:
                    print('Please introduce a number less or equal to {}'.format(player.money))
                else:
                    return bet
            except TypeError:
                print('Please enter a valid bet amount')
            
    def play(self):
        deck = Deck()
        deck.suffle()
        bet = self.place_bet()
        player_score = self.player.play(deck)

        if player_score > game_win_score:
            print('Player has miss, bank wins')
        else:
            bank_score = self.bank.play(deck, player_score)
            print('Bank score after play is {}'.format(bank_score))
            if bank_score >= player_score and bank_score <= game_win_score:
                print('Bank wins')
            else:
                self.player.game_won(bet * 2)
                print('Player wins {}, player has now {}'.format(bet, self.player.money))


print('Welcome to black jack')
is_accepted = False
amount = 0
while not is_accepted:
    try: 
        amount = int(input('How much money you want to bet today?'))
        if amount > 0:
            is_accepted = True
        else:
            print('Please enter a valid amount greater than 0')
    except TypeError:
        print('Please enter a valid amount')
        
player = Player(False, amount)
player_playing = True

def keep_playing():
    valid_answer = False
    answer = ''
    while not valid_answer:
        answer = input('Do you want to play another game? (y/n)').lower()
        if answer == 'y' or answer == 'n':
            valid_answer = True
    return answer == 'y'

while player_playing:
    clear_output()
    game = Game(player)
    game.play()
    if player.is_penniless():
        print('Sorry, your cash is over')
        player_playing = False
    else:
        player_playing = keep_playing()

print('Goodbye!')
