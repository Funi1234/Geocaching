# import LFSR
import numpy as np
from pylfsr import LFSR
import string
import Utils

import random



# GEOCACAHE
# 
# https://www.geocaching.com/geocache/GC7NE1Z
# 
# 


# unknown MSG 1 TX BEGINS 23:14:20Z
msg_1 = "00110 01100 01100 11000 11000 10111 11110 10010 01011 11100 01110 00110 01001 11100 11000 01000 01101 00011 00110 01100 10001 00110 00100 10111 11101 01011 11110 10110 11000 00000 00100 01100 10111 00100 01101 10100 11001 00111 11110 01011 10110 00111 11001 10011 10011 10010 00001 10011 11010 10001 11111 10000 00110 01110 10010 01000 11100 11001 00000 01111 10010 11100 11000 11111 11011 11001 00110 10011 01001 00001 01001 10000 10110 10101 10101 01100 10011 01001 00011 00001 11010 00100 00101 10010 00100 11001 10101 00001 11100 00111 01000 00001 01110 10110 11001 01001 11001 11100 01111 11100 01011 00011 01111 00011 10101 11001 00101 00011 11011 01101 10111 01011".replace(' ', '')
# Msg 2 TX BEGINS 23:15:11Z
msg_2 = "11011 11111 01110 10010 11101 11110 01011 00111 01001 00101 11001 10000 01111 10110 01010 10110 11001 11010 00100 10000 10101 00101 00011 00110 11100 01111 00010 11001 10101 00100 01011 10110 11111 00000 01011 11000 00010 10010 10000 10100 11100 10010 11111 01001 10110 10011 01010 01000 10101 01100 00111 01000 11011 11000 00110 10101 10101 11100 00100 10011 01100 01001 01110 11110 10001 01001 01001 01111 00011 11111 10000 10011 11100 10010 01110 01011 11110 11100 10101 10010 00010 10100 11010 10001 01100 01101 11000 10110 11001 00011 00110 00000 01110 00000 00101 00011 01110 10110 01110 01111 11000 10100 10001 11010 11101 10011 11100 00010 00100 11100 10000 11111".replace(' ', '')

# Now that was interesting... the last two messages, sent one after the other very late at night, had exactly the same length.
# Could it possibly be that a tired cypher clerk had slipped up and transmitted the same message twice?

if __name__ == "__main__":
    
    # Programatic
    bitwise_sum_of_the_adjacent_sections_of_key = Utils.xor_binary(msg_1, msg_2)

    print(bitwise_sum_of_the_adjacent_sections_of_key)

    state = [int(digit) for digit in  bitwise_sum_of_the_adjacent_sections_of_key[:61][::-1]]

    poly = [3, 7, 12, 15, 16, 27, 30, 31, 37, 38, 41, 43, 45, 48, 49, 51, 52, 54, 57, 59, 60, 61]
    # The taps need to be highest to lowest, apparently, for the library.
    fpoly = poly[::-1]

    keys = []

    L = LFSR(fpoly=fpoly, initstate=state, verbose=False)
    with open('filename.txt', 'w') as file:
        for i in range(10000):
            tempseq = L.runKCycle(len(msg_1))
            key = "".join([str(x) for x in tempseq])
            if i % 100 == 0:
                print()
            print(".", end="")
            file.write(key)
            keys.append(key)
    
    # print()
    # print("Starting")
    # for i in range(len(keys) - 1):
    #     if Utils.xor_binary(keys[i], keys[i+1]) == bitwise_sum_of_the_adjacent_sections_of_key:
    #         print(keys[i], keys[i+1])
    #     if Utils.xor_binary(keys[i], keys[i+1]) == bitwise_sum_of_the_adjacent_sections_of_key[::-1]:
    #         print("reversed")
    #         print(keys[i], keys[i+1])



    # init_state = bitwise_sum_of_the_adjacent_sections_of_key[:61][::-1]

    # key1 = Utils.lfsr_backwards(fpoly, len(msg_1)+len(msg_2),'', init_state)
    # key2 = Utils.lfsr_backwards(fpoly, len(msg_2),'', init_state)

    # key = Utils.xor_binary(key1, key2)

    # y = Utils.xor_binary(key, msg_2)

    # print(Utils.decode_baudot(y))
    # print()




# # TESTING
# L = LFSR(fpoly=fpoly, initstate=state, verbose=False)
#     tempseq = L.runKCycle(len(msg_2))
#     key = "".join([str(x) for x in tempseq])