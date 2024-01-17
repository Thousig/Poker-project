#from icecream import ic
def is_high_card(hand):

    hand = sorted(hand)
    highest = hand[0]

    for card in hand:
        if card in range(13):
            if card > highest:
                highest = card
        if card in range(13,26):
            if card-13 > highest:
                highest = card-13
        if card in range(26,39):
            if card - 26 > highest:
                highest = card-26
        if card in range(39,52):
            if card - 39 > highest:
                highest = card-39
    return highest

def evaluator(numbers):
    count_hearts = count_diamonds = count_spades = count_clubs = 0
    numbers = sorted(numbers)
    for i, j in enumerate(numbers):
        #ic(numbers[i]+1 in numbers and numbers[i]+2 in numbers and numbers[i]+3 in numbers and numbers[i]+4 in numbers, numbers[i:i+5])
        if numbers[i]+1 in numbers and numbers[i]+2 in numbers and numbers[i]+3 in numbers and numbers[i]+4 in numbers:
            
            #count if it is a straight flush or just a straight, count suits
            count_hearts = count_diamonds = count_spades = count_clubs = 0
            for k in numbers[i:i+5]:    
                
                if k in range(13):
                    count_hearts +=1
                    if count_hearts == 5:
                        return (8, k%13+2)

                if k in range(13,26):
                    count_diamonds +=1
                    if count_diamonds == 5:
                        return (8, k%13+2)
                    
                if k in range(26,39):
                    count_spades +=1
                    if count_spades == 5:
                        return (8, k%13+2)
                    
                if k in range(39,52):
                    count_clubs +=1
                    if count_clubs == 5:
                        return (8, k%13+2)
                    
        #Flush
        #Count suits for Flush

        if j in range(13):
            count_hearts +=1
            #ic(count_hearts)
            if count_hearts == 5:
                return (5, j%13+2)

        if j in range(13,26):
            count_diamonds +=1
            if count_diamonds == 5:
                return (5, j%13+2)
            
        if j in range(26,39):
            count_spades +=1
            #ic(count_spades)
            if count_spades == 5:
                return (5, j%13+2)
            
        if j in range(39,52):
            count_clubs +=1
            if count_clubs == 5:
                return (5, j%13+2)

        
        #Straight
        count_cards_in_a_row = 1
        for t in range(len(numbers)):
            #ic(j+count_cards_in_a_row in numbers, j+count_cards_in_a_row+13 in numbers, j+count_cards_in_a_row+26 in numbers, j+count_cards_in_a_row+39 in numbers )
            if j+count_cards_in_a_row in numbers or j+count_cards_in_a_row+13 in numbers or j+count_cards_in_a_row+26 in numbers or j+count_cards_in_a_row+39 in numbers or j+count_cards_in_a_row-13 in numbers or j+count_cards_in_a_row-26 in numbers or j+count_cards_in_a_row-39 in numbers:
                count_cards_in_a_row += 1
                #ic(count_cards_in_a_row, j)
                if count_cards_in_a_row >= 5:
                    return (4, (j+4)%13+2)
        

            
    # Four of a kind      
    for h in range(13):
        if (h in numbers) and (h+13 in numbers) and (h+26 in numbers) and (h+39 in numbers):
            higest_card=h
            return (7,h%13+2)
    
    # Full house  
    numbers_of_pairs1 = 0
    for i in range(13):
        if ((i +13  in numbers) and (i + 26 in numbers) and (i + 39 in numbers)
            or (i in numbers)and (i + 26 in numbers) and (i + 39 in numbers)
            or (i in numbers) and (i +13  in numbers) and (i + 39 in numbers)
            or (i in numbers) and (i +13  in numbers) and (i + 26 in numbers)):
            three_of_kind_number = i
            for i in range(13):
                if ((i in numbers) and (i + 13 in numbers)
                    or (i in numbers) and (i + 26 in numbers)
                    or (i in numbers) and (i + 39 in numbers)
                    or (i +13 in numbers) and (i + 26 in numbers)
                    or (i + 13  in numbers) and (i + 39 in numbers)
                    or (i + 26 in numbers) and (i + 39 in numbers)):
                    numbers_of_pairs1 += 1
    if numbers_of_pairs1 >=2:
        return (6,three_of_kind_number)
            
                    
    
    #3 of a kind
    for i in range(13):
        if ((i +13  in numbers) and (i + 26 in numbers) and (i + 39 in numbers)
            or (i in numbers)and (i + 26 in numbers) and (i + 39 in numbers)
            or (i in numbers) and (i +13  in numbers) and (i + 39 in numbers)
            or (i in numbers) and (i +13  in numbers) and (i + 26 in numbers)):
            return (3,i)   
    
    #2 pairs
    numbers_of_pairs = 0
    highest_pair = 0    
    for i in range(13):
        if ((i in numbers) and (i + 13 in numbers)
            or (i in numbers) and (i + 26 in numbers)
            or (i in numbers) and (i + 39 in numbers)
            or (i +13 in numbers) and (i + 26 in numbers)
            or (i + 13  in numbers) and (i + 39 in numbers)
            or (i + 26 in numbers) and (i + 39 in numbers)):
            if i > highest_pair:
                highest_pair = i
            numbers_of_pairs += 1
            
    #2 pairs        
    if numbers_of_pairs >= 2:
        return (2,highest_pair) 
        
    #2 of a kind (Pair)
    if numbers_of_pairs == 1:
            return (1,highest_pair)
    
           
    return (0, is_high_card(numbers))



if __name__ == "__main__":
    bot_cards = [0, 1, 15, 16, 7, 42, 2]
    ai_cards = [1, 14, 10, 23, 36, 48, 46]
    #if evaluator(ai_cards) == 0:
        #ic(is_high_card(ai_cards))
        
    print(evaluator(ai_cards))