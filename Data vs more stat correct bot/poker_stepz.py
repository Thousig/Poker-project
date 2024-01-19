#import random
import numpy as np

from collections import deque

from evaluation import evaluator
from poker_bot_2 import turn_one_bot_2, turn_two_bot_2, turn_three_bot_2, turn_four_bot_2
from game import Deck
from game import Poker
#from game import actions, has_no_points_left
from poker_bot import turn_one_bot, turn_two_bot, turn_three_bot, turn_four_bot

# Global variables
# render = True



class MasterGame:

    def __init__(self):
        self.betting_amount = 1
        self.balance_amount = 10
        self.bot_has_betted = False
        self.ai_has_betted = False
        self.round = -1
        self.bot = self.ai = self.balance_amount
        self.ai_start_round_balance = self.ai
        self.game = Poker()
        self.Deck = Deck()
        self.table_amount = 0
        self.done = False
        self.turn_count = 1
        self.part_turn_counter = 0
        self.AI_hand = self.bot_hand = []

    def win_check(self):
        return self.ai != 0 and self.bot != 0

    def turn_one_part_one(self):
        self.turn_count +=1
        self.round += 1

        #print(f'AI balance: {self.ai}')
        #print(f'Bot balance: {self.bot}')
        
        # set has betted to False
        self.ai_has_betted = False
        self.bot_has_betted = False

        # resetting the table amount
        self.table_amount = 0

        # Dealing two cards to both the self.ai and the self.bot



        # Turn 1
        # Choosing who is the blind. The blind has to throw 1.
        
        if self.round % 2 == 0: # self.bot is the blind
            self.bot -= self.betting_amount
            self.table_amount += self.betting_amount
            self.bot_has_betted = True
            ##print('self.bot has betted 1 point')
        
        else: # self.ai is the blind
            self.ai -= self.betting_amount
            self.table_amount += self.betting_amount
            self.ai_has_betted = True
            ##print('self.ai has betted 1 point')

        return self.bot_has_betted

        
    def turn_one_part_two(self, ai_action):        
        
        # If self.bot is blind, self.ai has to decide wether it wants to call or fold.
        if self.round % 2 == 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai_has_betted = True
                self.ai -= 1
                self.table_amount += 1
                ##print('AI has betted 1 point\n')
            elif act_ai == -1:
                self.bot += self.table_amount
                ##print('Bot won this self.round\n')
                self.done = True
                return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)


        # If self.ai is blind, self.bot has to decide wether it wants to call or fold.
        if self.round % 2 != 0: 
            #act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_one_bot_2(self.bot_hand)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                ##print('self.bot has betted 1 point\n')
            elif act_bot == -1: # self.ai folds
                self.ai += self.table_amount
                ##print('Bot folded, AI won this self.round, 1\n')
                self.done = True
                return ((np.zeros(105), self.ai - self.ai_start_round_balance, self.done))
        


        
        self.game.show_hands()
        self.game.the_flop()
        self.game.show_cards_on_table()

        self.ai_has_betted = False
        self.bot_has_betted = False

        if self.round % 2 == 0:
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_two_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point\n')
            elif act_bot == 0:
                ##print('Bot checks, 1\n')
                pass

        return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
            
        
                
                # reset has betted flags and the amount of points on the table
    def turn_two_part_one(self, ai_action):
        
        # Turn 2
        ##print('Turn 2')
        # Deal three cards to the table


        # If self.ai's turn, self.ai decides if it wants to raise or check, then self.bot does the same
        if self.round % 2 != 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                self.ai_has_betted = True
                ##print('AI has betted 1 point\n')
            elif act_ai == 0:
                ##print('AI checks\n')
                pass
                
            
        # AI has to decide wether to call or fold
        if self.round % 2 == 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                ##print('AI has betted 1 point\n')
            elif act_ai == -1:
                self.bot += self.table_amount
                ##print('Bot won this self.round\n')
                self.done = True
                return ((np.zeros(105), self.ai - self.ai_start_round_balance, self.done))
            

        # Bot has to decide wether it wants to call or fold.
                self.table_amount += 1
                self.ai_has_betted = True
        if self.round % 2 != 0: 
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_two_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point\n')
            elif act_bot == -1: # self.ai folds
                self.ai += self.table_amount
                ##print('AI won this self.round, self.bot folded\n')
                self.done = True
                return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)
            
        
        
        if self.ai_has_betted != self.bot_has_betted:
            if self.bot_has_betted == True:
                self.part_turn_counter = 1 #husk at kører turn two part two funktionen og step hvis dette sker, ikke ny turn
                return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
            
            else:
                self.turn_two_part_two(None)
                
        
        self.ai_has_betted = False
        self.bot_has_betted = False

        self.game.the_turn()
        self.game.show_cards_on_table()

        self.game.show_hands()
        if self.done == True:
            return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)
        self.turn_count += 1
        # If self.bot's turn, self.bot decides if it wants to raise or check, then self.ai does the same
        if self.round % 2 == 0:
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_three_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point\n')
            elif act_bot == 0:
                ##print('Bot checks, 2\n')
                pass
        return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
            
        
    def turn_two_part_two(self, ai_action):
        

        if self.ai_has_betted != self.bot_has_betted:
            if self.ai_has_betted == False:
                # AI has to decide wether to call or fold
                act_ai = ai_action
                if act_ai == 1:
                    self.ai -= 1
                    self.ai_has_betted = True
                    self.table_amount += 1
                    ##print('AI has betted 1 point\n')
                    self.ai_has_betted = False
                    self.bot_has_betted = False

                    self.game.the_turn()
                    self.game.show_cards_on_table()

                    self.game.show_hands()
                            # If self.bot's turn, self.bot decides if it wants to raise or check, then self.ai does the same
                    if self.round % 2 == 0:
                        # act_bot = actions('self.bot',self.ai_has_betted)
                        act_bot = turn_three_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
                        if act_bot == 1:
                            self.bot -= 1
                            self.table_amount += 1
                            self.bot_has_betted = True
                            ##print('self.bot has betted 1 point\n')
                            return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
                        elif act_bot == 0:
                            ##print('Bot checks, 3\n')
                            pass
                    return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
                elif act_ai == -1:
                    self.bot += self.table_amount
                    ##print('Bot won this self.round\n')
                    self.done = True
                    return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)
            else:
                # Bot has to decide wether it wants to call or fold.
                # act_bot = actions('self.bot',self.ai_has_betted)
                act_bot = turn_two_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
                if act_bot == 1:
                    self.bot -= 1
                    self.table_amount += 1
                    self.ai_has_betted = False
                    self.bot_has_betted = False

                    self.game.the_turn()
                    self.game.show_cards_on_table()

                    self.game.show_hands()
                    ##print('self.bot has betted 1 point\n')
                    return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
                elif act_bot == -1: # self.ai folds
                    self.ai += self.table_amount
                    ##print('Bot folded, AI won this self.round, 2\n')
                    self.done = True
                    return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)


        ##print(f'Amount on table: {self.table_amount}\n')



            
    def turn_three_part_one(self, ai_action):
        

        # If self.ai's turn, self.bot decides if it wants to raise or check, then self.bot does the same
        if self.round % 2 != 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                self.ai_has_betted = True
                ##print('AI has betted 1 point\n')
            elif act_ai == 0:
                ##print('AI checks\n')
                pass
                

        # AI has to decide wether to call or fold
        if self.round % 2 == 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                self.ai_has_betted = True
                ##print('AI has betted 1 point\n')
            elif act_ai == -1:
                self.bot += self.table_amount
                self.done = True
                ##print('Bot won this self.round\n')
                return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)

        # Bot has to decide wether it wants to call or fold.
        if self.round % 2 != 0: 
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_three_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point\n')
            elif act_bot == -1: # self.ai folds
                self.ai += self.table_amount
                ##print('Bot folded, AI won this self.round, 3\n')
                self.done = True
                ##print('linje 316')
                return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)
            
        if self.ai_has_betted != self.bot_has_betted:
            if self.bot_has_betted == True:
                self.part_turn_counter = 1 #husk at kører turn two part two funktionen og step hvis dette sker, ikke ny turn
                return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))
            
            else:
                return self.turn_three_part_two(None)
                
            
        self.ai_has_betted = False
        self.bot_has_betted = False

        self.game.the_turn()
        self.game.show_cards_on_table()

        self.game.show_hands()
        if self.round % 2 == 0:
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_four_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point\n')
            elif act_bot == 0:
                ##print('Bot checks, 4\n')
                pass
    
        elif act_ai == -1:
            self.bot += self.table_amount
            ##print('Bot won this self.round\n')
        if self.done == True:
            return (np.zeros(105), self.ai - self.ai_start_round_balance, self.done)
        self.turn_count += 1

        #bot action turn 4 start

        return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done))    

        
    def turn_three_part_two(self, ai_action):
        
        if self.ai_has_betted != self.bot_has_betted:
            if self.ai_has_betted == False:
                # AI has to decide wether to call or fold
                act_ai = ai_action
                if act_ai == 1:
                    self.ai -= 1
                    self.table_amount += 1
                    self.ai_has_betted = True

                    self.ai_has_betted = False
                    self.bot_has_betted = False

                    self.game.the_turn()
                    self.game.show_cards_on_table()

                    self.game.show_hands()

                    if self.round % 2 == 0:
                        # act_bot = actions('self.bot',self.ai_has_betted)
                        act_bot = turn_four_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
                        if act_bot == 1:
                            self.bot -= 1
                            self.table_amount += 1
                            self.bot_has_betted = True
                            ##print('self.bot has betted 1 point\n')
                        elif act_bot == 0:
                            ##print('Bot checks, 5\n')
                            pass
                    return ((np.append(self.game.state(), self.bot_has_betted), 0, self.done)) 
                
                elif act_ai == -1:
                    self.bot += self.table_amount
                    ##print('Bot won this self.round\n')
                    self.done = True
                    return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)
            else:
                # Bot has to decide wether it wants to call or fold.
                # act_bot = actions('self.bot',self.ai_has_betted)
                act_bot = turn_three_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
                if act_bot == 1:
                    self.bot -= 1
                    self.table_amount += 1
                    self.bot_has_betted = True
                    ##print('self.bot has betted 1 point\n')
                    return (np.append(self.game.state(), self.bot_has_betted), 0, self.done)
                elif act_bot == -1: # self.ai folds
                    self.ai += self.table_amount
                    ##print('Bot folded, AI won this self.round, 4\n')
                    self.done = True
                    return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)
                


        # reset has betted flags and the amount of points on the table
        
    def turn_four_part_one(self, ai_action):
        self.part_turn_counter = 0

        # If self.ai's turn, self.bot decides if it wants to raise or check, then self.bot does the same
        if self.round % 2 != 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                self.ai_has_betted = True
                ##print('AI has betted 1 point\n')
            elif act_ai == 0:
                ##print('AI checks\n')
                pass
                
                
        # AI has to decide wether to call or fold
        if self.round % 2 == 0:
            act_ai = ai_action
            if act_ai == 1:
                self.ai -= 1
                self.table_amount += 1
                self.ai_has_betted = True
                ##print('AI has betted 1 point\n')
                return self.show_off()
            elif act_ai == -1:
                self.bot += self.table_amount
                ##print('Bot won this self.round\n')
                self.done = True
                return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)

        # Bot has to decide wether it wants to call or fold.
        if self.round % 2 != 0: 
            # act_bot = actions('self.bot',self.ai_has_betted)
            act_bot = turn_four_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
            if act_bot == 1:
                self.bot -= 1
                self.table_amount += 1
                self.bot_has_betted = True
                ##print('self.bot has betted 1 point, 12\n')
                return self.show_off()
            elif act_bot == -1: # self.bot folds
                self.ai += self.table_amount
                ##print('ai won this self.round\n')
                self.done = True
                return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)
            
        if self.ai_has_betted != self.bot_has_betted:
            if self.bot_has_betted == True:
                self.part_turn_counter = 1 #husk at kører turn two part two funktionen og step hvis dette sker, ikke ny turn
                return ((np.append(self.game.state(), self.bot_has_betted), self.ai - self.ai_start_round_balance, self.done))
            
            else:
                return self.turn_four_part_two(None)

        return self.show_off()

    def turn_four_part_two(self, ai_action):

        if self.ai_has_betted != self.bot_has_betted:
            if self.ai_has_betted == False:
                # AI has to decide wether to call or fold
                act_ai = ai_action
                if act_ai == 1:
                    self.ai -= 1
                    self.ai_has_betted = True
                    self.table_amount += 1
                    ##print('AI has betted 1 point\n')
                    ##print('hej')
                    return self.show_off()
                elif act_ai == -1:
                    self.bot += self.table_amount
                    #print('Bot won this self.round\n')
                    self.done = True
                    return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)
            else:
                # Bot has to decide wether it wants to call or fold.
                # act_bot = actions('self.bot',self.ai_has_betted)
                act_bot = turn_four_bot_2(self.game.merge_bot_and_table(), self.ai_has_betted)
                if act_bot == 1:
                    self.bot -= 1
                    self.table_amount += 1
                    #print('self.bot has betted 1 point\n')
                    #print('hej2')
                    return self.show_off()
                elif act_bot == -1: # self.ai folds
                    self.ai += self.table_amount
                    #print('Bot won this self.round\n')
                    self.done = True
                    return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)
                
    def show_off(self):
        #print('fjjsj')
        #print(f'Amount on table: {self.table_amount}')

        # Now evaluate the players hand
        # Determining winner

        self.game.show_cards_on_table()
        self.game.show_hands()
        self.game.show_cards_on_table()
        self.game.show_hands()

        winner = self.game.winner() 
        if winner == True:
            self.ai += self.table_amount
            #print('AI wins\n')
        elif winner == False:
            self.bot += self.table_amount
            #print('Bot wins\n')
        else:
            #print('No winner\n')
            self.ai += self.table_amount/2
            self.bot += self.table_amount/2
        self.done = True
        return ((np.zeros(105)), self.ai - self.ai_start_round_balance, self.done)

    
    def reset(self):
        del(self.game)
        self.game = Poker()
        self.turn_count = 1
        self.AI_hand = self.bot_hand = []
        self.AI_hand, self.bot_hand = self.game.deal_hands()
        self.game.table_cards = []
        self.ai = self.bot = 4
        self.ai_start_round_balance = self.ai
        self.table_amount = 0
        self.done = False
        return ((np.append(self.game.state(), self.bot_has_betted))) 


    def step(self, AIs_actions):
        #print(f"AI: {self.AI_hand}, BOT: {self.bot_hand}\n table: {self.game.table_cards}")
        #print(self.turn_count)
        if self.turn_count == 1:
            if self.turn_one_part_one() == False:
                return self.turn_one_part_two(None)
            else:
                return self.turn_one_part_two(AIs_actions) #mangler at lave action funktion

        elif self.turn_count == 2:
            if self.part_turn_counter == 0:
                return self.turn_two_part_one(AIs_actions)
            elif self.part_turn_counter == 1:
                self.part_turn_counter = 0
                self.turn_count +=1
                return self.turn_two_part_two(AIs_actions)
            
        elif self.turn_count == 3:
            if self.part_turn_counter == 0:
                return self.turn_three_part_one(AIs_actions)
            elif self.part_turn_counter == 1:
                self.part_turn_counter = 0
                self.turn_count +=1
                return self.turn_three_part_two(AIs_actions)
            
        elif self.turn_count == 4:
            if self.part_turn_counter == 0:
                return self.turn_four_part_one(AIs_actions)
            elif self.part_turn_counter == 1:
                self.part_turn_counter = 0
                self.turn_count +=1
                return self.turn_four_part_two(AIs_actions)

        

           
if __name__=='__main__':
    #print('START\n')
    mastergame = MasterGame()
    mastergame.reset()
    for i in range(100):
        if len(mastergame.game.table_cards) > 5:
            mastergame.show_off()
        if mastergame.done == True or mastergame.turn_count == 5:
            mastergame.reset()
            #print("reset")
        else:
            
            #print(mastergame.step(1))
            
            #print(mastergame.done)
            pass