import random
from evaluation import evaluator
import numpy as np

class Deck:
    """class to represent the deck"""

    def __init__(self):
        # represents the cards as 0-51
        # hearts: 0-12; diamonds: 13-25; spades: 26-38; clubs: 39-51
        self.deck = list(range(0,52))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        # if deck is longer than 0, pop off the deal the top card
        if len(self.deck) == 0:
            return None
        else:
            return self.deck.pop(0)
        
    def reset_deck(self):
        self.deck = list(range(52))


class Poker:
    """class to represent the cards of player1, player2 and the table"""

    def __init__(self):
        """Get the deck and shuffle it. Create two empty hands"""
        self.Deck = Deck()
        self.Deck.shuffle()
        self.AI_hand = []
        self.bot_hand = []
        self.table_cards = []
  


    def deal_hands(self):
        self.AI_hand = []
        self.bot_hand = []
        # Deal two cards to each player
        for i in range(2):
            self.AI_hand.append(self.Deck.deal())
            self.bot_hand.append(self.Deck.deal())
        return self.AI_hand, self.bot_hand




    def the_flop(self):
        for i in range(3):
            self.table_cards.append(self.Deck.deal())
        #self.print_flop = ''
        #for card in self.table_cards:
        #    self.print_flop += str(card) + ' '
        #print(f'cards on the table {self.print_flop}')

    
    def the_turn(self):
        new_card = self.Deck.deal()
        self.table_cards.append(new_card)
        #self.print_flop += str(new_card) + ' '
        #print(f'Cards on the table: {self.print_flop} ')

    def show_cards_on_table(self):
        print_cards = ''
        for card in self.table_cards:
            print_cards += str(card) + ' '
        #print(f'Cards on the table: {print_cards}')


    def merge_ai_and_table(self):
        for i in self.table_cards:
            self.AI_hand.append(i)
        return self.AI_hand

    def merge_bot_and_table(self):
        merged = self.bot_hand + self.table_cards
        return merged
    
    def winner(self):

        self.AI_hand += self.table_cards 
        self.bot_hand += self.table_cards

        #print(f'AI score: {evaluator(self.AI_hand)}, Bot score: {evaluator(self.bot_hand)}')

        if evaluator(self.AI_hand)[0] > evaluator(self.bot_hand)[0]:
            return True
        elif evaluator(self.AI_hand)[0] < evaluator(self.bot_hand)[0]:
            return False
        else:
            if evaluator(self.AI_hand)[1] > evaluator(self.bot_hand)[1]:
                return True
            elif evaluator(self.AI_hand)[1] < evaluator(self.bot_hand)[1]:
                return False
            else:
                return -1

    def show_hands(self):
        #print(f'AI hand: {self.AI_hand}, Bot hand: {self.bot_hand}')
        pass

    def state(self):
        self.converted_ai_hand = np.zeros(104)
        for i in range(len(self.converted_ai_hand)):
            if i in self.AI_hand:
                self.converted_ai_hand[i] = 1
            elif i in self.table_cards:
                self.converted_ai_hand[i+52] = 1
        return self.converted_ai_hand


    










    


def bet_check(round, ai, bot, table_amount):
    updated_round = round+1
    if round % 2 == 0:
        act_bot = actions('bot',False)
        if act_bot == 1:
            bot -= 1
            table_amount += 1
            #print('bot has betted 1 point\n')
            return updated_round, ai, bot, table_amount
        elif act_bot == 0:
            #print('Bot checks\n')
            return updated_round
    # If ai's turn, bot decides if it wants to raise or check, then bot does the same
    else:
        act_ai = actions('AI',False)
        if act_ai == 1:
            ai -= 1
            table_amount += 1
            ai_has_betted = True
            #print('AI has betted 1 point\n')

            return round, ai, bot, table_amount
        elif act_ai == 0:
            #print('AI checks\n')
            return updated_round



def call_fold(round, ai, bot, table_amount):

    updated_round = round + 1
    # AI has to decide wether to call or fold
    if round % 2 != 0:
        act_ai = actions('AI',True)
        if act_ai == 1:
            ai -= 1
            table_amount += 1
            #print('AI has betted 1 point\n')
            return updated_round, ai, bot, table_amount
        elif act_ai == -1:
            bot += table_amount
            #print('Bot won this round\n')
            return updated_round, bot

    # Bot has to decide wether it wants to call or fold.
    if round % 2 == 0: 
        act_bot = actions('bot',True)
        if act_bot == 1:
            bot -= 1
            table_amount += 1
            #print('bot has betted 1 point\n')
            return updated_round, ai, bot, table_amount
        elif act_bot == -1: # ai folds
            ai += table_amount
            #print('Bot won this round\n')
            return updated_round, ai, bot
    






def actions(player, other_has_betted):

    if other_has_betted:
        bet_fold = input(f'Do {player} want to bet or fold? (b/f) ')
        if bet_fold == 'b':
            return 1 # 1 means bet
        else:
            return -1 # -1 means fold
    else:
        bet_check = input(f'Do {player} want to bet or check? (b/c) ')
        if bet_check == 'b':
            return 1 # 1 means bet
        else:
            return 0 # 0 means check
        
def has_no_points_left(ai, bot):
    #print()
    if ai == 0:
        return True
    if bot == 0:
        return True








