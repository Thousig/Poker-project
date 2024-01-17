def turn_one_bot(hand):
    #if the bot has a pair on hand in first turn, its gonna bet
    hand = sorted(hand)
    hand_of_pairs = 0    
    for i in range(13):
        if ((i in hand) and (i + 13 in hand)
            or (i in hand) and (i + 26 in hand)
            or (i in hand) and (i + 39 in hand)
            or (i +13 in hand) and (i + 26 in hand)
            or (i + 13  in hand) and (i + 39 in hand)
            or (i + 26 in hand) and (i + 39 in hand)): 
            hand_of_pairs += 1
    if hand_of_pairs >=1:
        return 1

    #if it has two of same suit it bets
    count_hearts = count_diamonds = count_spades = count_clubs = 0
    for i, j in enumerate(hand):
        if j in range(13):
            count_hearts +=1
            if count_hearts == 2:
                return 1

        if j in range(13,26):
            count_diamonds +=1
            if count_diamonds == 2:
                return 1
            
        if j in range(26,39):
            count_spades +=1
            if count_spades == 2:
                return 1
            
        if j in range(39,52):
            count_clubs +=1
            if count_clubs == 2:
                return 1
        
        #if it has an ace, king or queen it bets
        if j in range(10,13) or j in range(23,26) or j in range(36,39) or j in range(49,52):
            return 1
        
    
        #Straight draws, if it has like ace 2 off suit it will bet
        count_cards_in_a_row = 1
        for t in range(len(hand)-1):
            if j+count_cards_in_a_row in hand or j+count_cards_in_a_row+13 in hand or j+count_cards_in_a_row+26 in hand or j+count_cards_in_a_row+39 in hand or j+count_cards_in_a_row-13 in hand or j+count_cards_in_a_row-26 in hand or j+count_cards_in_a_row-39 in hand:
                count_cards_in_a_row += 1
                if count_cards_in_a_row >= 2:
                    return 1
    
    #else it folds, unless it is the blind
    else:
        return -1
    
    

    
def turn_two_bot(hand, ai_has_betted):
    #if the bot has a pair, its gonna bet
    hand = sorted(hand)
    hand_of_pairs = 0    
    for i in range(13):
        if ((i in hand) and (i + 13 in hand)
            or (i in hand) and (i + 26 in hand)
            or (i in hand) and (i + 39 in hand)
            or (i +13 in hand) and (i + 26 in hand)
            or (i + 13  in hand) and (i + 39 in hand)
            or (i + 26 in hand) and (i + 39 in hand)): 
            hand_of_pairs += 1
    if hand_of_pairs >=1:
        return 1

    #if it has four of same suit it bets
    count_hearts = count_diamonds = count_spades = count_clubs = 0
    for i, j in enumerate(hand):
        if j in range(13):
            count_hearts +=1
            if count_hearts == 4:
                return 1

        if j in range(13,26):
            count_diamonds +=1
            if count_diamonds == 4:
                return 1
            
        if j in range(26,39):
            count_spades +=1
            if count_spades == 4:
                return 1
            
        if j in range(39,52):
            count_clubs +=1
            if count_clubs == 4:
                return 1
        
    
        #Straight draws, if it has like ace two three four off suit it will bet
        count_cards_in_a_row = 1
        for t in range(len(hand)-1):
            if j+count_cards_in_a_row in hand or j+count_cards_in_a_row+13 in hand or j+count_cards_in_a_row+26 in hand or j+count_cards_in_a_row+39 in hand or j+count_cards_in_a_row-13 in hand or j+count_cards_in_a_row-26 in hand or j+count_cards_in_a_row-39 in hand:
                count_cards_in_a_row += 1
                if count_cards_in_a_row >= 4:
                    return 1
                
    #if the ai has checked or if it is the bots turn to start and does not want to bet, but does not fold unlees it is nessesary
    if ai_has_betted == False:
        return 0
    
    #it folds when it does not have anything good and the AI has betted
    else:
        return -1
    
    
if __name__ == "__main__":
    cards = [0, 3, 5, 7, 9]
    
def turn_three_bot(hand, ai_has_betted):
    #if the bot has two pair, its gonna bet
    hand = sorted(hand)
    hand_of_pairs = 0    
    for i in range(13):
        if ((i in hand) and (i + 13 in hand)
            or (i in hand) and (i + 26 in hand)
            or (i in hand) and (i + 39 in hand)
            or (i +13 in hand) and (i + 26 in hand)
            or (i + 13  in hand) and (i + 39 in hand)
            or (i + 26 in hand) and (i + 39 in hand)): 
            hand_of_pairs += 1
    if hand_of_pairs >=2:
        return 1
    
    # if 3 of a kind, its gonna bet
    for i in range(13):
        if ((i +13  in hand) and (i + 26 in hand) and (i + 39 in hand)
            or (i in hand)and (i + 26 in hand) and (i + 39 in hand)
            or (i in hand) and (i +13  in hand) and (i + 39 in hand)
            or (i in hand) and (i +13  in hand) and (i + 26 in hand)):
            return 1   

    #if it has four of same suit it bets
    count_hearts = count_diamonds = count_spades = count_clubs = 0
    for i, j in enumerate(hand):
        if j in range(13):
            count_hearts +=1
            if count_hearts >= 4:
                return 1

        if j in range(13,26):
            count_diamonds +=1
            if count_diamonds >= 4:
                return 1
            
        if j in range(26,39):
            count_spades +=1
            if count_spades >= 4:
                return 1
            
        if j in range(39,52):
            count_clubs +=1
            if count_clubs >= 4:
                return 1
        
    
        #Straight draws, if it has like ace two three four off suit it will bet
        count_cards_in_a_row = 1
        for t in range(len(hand)-1):
            if j+count_cards_in_a_row in hand or j+count_cards_in_a_row+13 in hand or j+count_cards_in_a_row+26 in hand or j+count_cards_in_a_row+39 in hand or j+count_cards_in_a_row-13 in hand or j+count_cards_in_a_row-26 in hand or j+count_cards_in_a_row-39 in hand:
                count_cards_in_a_row += 1
                if count_cards_in_a_row >= 4:  
                    return 1
                
    #if the ai has checked or if it is the bots turn to start and does not want to bet, but does not fold unlees it is nessesary
    if ai_has_betted == False:
        return 0
    
    #it folds when it does not have anything good and the AI has betted
    else:
        return -1
    
    
if __name__ == "__main__":
    cards = [3, 16, 29, 14, 13, 12]
    
    
    
def turn_four_bot(hand, ai_has_betted):
    #if the bot has two pair, its gonna bet
    hand = sorted(hand)
    hand_of_pairs = 0    
    for i in range(13):
        if ((i in hand) and (i + 13 in hand)
            or (i in hand) and (i + 26 in hand)
            or (i in hand) and (i + 39 in hand)
            or (i +13 in hand) and (i + 26 in hand)
            or (i + 13  in hand) and (i + 39 in hand)
            or (i + 26 in hand) and (i + 39 in hand)): 
            hand_of_pairs += 1
    if hand_of_pairs >=2:
        return 1
    
    # if 3 of a kind, its gonna bet
    for i in range(13):
        if ((i +13  in hand) and (i + 26 in hand) and (i + 39 in hand)
            or (i in hand)and (i + 26 in hand) and (i + 39 in hand)
            or (i in hand) and (i +13  in hand) and (i + 39 in hand)
            or (i in hand) and (i +13  in hand) and (i + 26 in hand)):
            return 1   

    #if it has four of same suit it bets
    count_hearts = count_diamonds = count_spades = count_clubs = 0
    for i, j in enumerate(hand):
        if j in range(13):
            count_hearts +=1
            if count_hearts >= 5:
                return 1

        if j in range(13,26):
            count_diamonds +=1
            if count_diamonds >= 5:
                return 1
            
        if j in range(26,39):
            count_spades +=1
            if count_spades >= 5:
                return 1
            
        if j in range(39,52):
            count_clubs +=1
            if count_clubs >= 5:
                return 1
        
    
        #Straight draws, if it has like ace two three four off suit it will bet
        count_cards_in_a_row = 1
        for t in range(len(hand)-1):
            if j+count_cards_in_a_row in hand or j+count_cards_in_a_row+13 in hand or j+count_cards_in_a_row+26 in hand or j+count_cards_in_a_row+39 in hand or j+count_cards_in_a_row-13 in hand or j+count_cards_in_a_row-26 in hand or j+count_cards_in_a_row-39 in hand:
                count_cards_in_a_row += 1
                if count_cards_in_a_row >= 5:  
                    return 1
                
    #if the ai has checked or if it is the bots turn to start and does not want to bet, but does not fold unlees it is nessesary
    if ai_has_betted == False:
        return 0


    #it folds when it does not have anything good and the AI has betted
    else:
        return -1
    
    
if __name__ == "__main__":
    cards = [3, 16, 29, 14, 13, 12, 10]
