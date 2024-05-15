# import LFSR
from pylfsr import LFSR
import Utils


# GEOCACAHE
# 
# https://www.geocaching.com/geocache/GC7NE1M
# 
# 


# unknown MSG 1 TX BEGINS 11:43:20Z
msg_1 = "00010 11001 00110 01010 11000 11000 10000 00101 00111 10111 00010 11101 11010 10000 01010 10001 10010 01010 10001 10000 10100 11010 01011 11110 11011 10001 11110 00110 01110 10011 11100 11010 11101 10111 00100 00100 01010 10100 00011 10100 01111 01000 01000 00000 10001 10110 00010 10010 01000 01000 00111 01011 00010 00000 01011 11000 00110 01010 10110 00100 01110 00100 11111 01011 10010 01101 01000 11010 01101 00110 11000 10011 10100 01111 10010 11011 10011 00010 01011 10010 11111 10111 00100 00110 10001 10110 10101 01101 01100 11011 10110 01010 01110 00010 01110 01001 10010 10101 01111 10111 00111 00000 10001 01011 11101 00101 10000 01001 11001 10011 11100".replace(' ', '')
# Msg 2 TX BEGINS 13:00:00Z - Weather Report?
msg_2 = "10000 11010 10010 10011 10010 00010 01111 00010 10010 11000 10100 01100 00101 00000 01010 11111 11001 10010 11001 11010 01000 11001 01001 10101 11101 01101 00011 01100 11010 11010 01010 00100 11000 01001 11101 01101 00110 11111 11010 01111 11101 00110 10110 01100 01101 11000 01101 11010 00000 10101 11011 00100 00001 10100 11111 11001 11110 11101 00011 00000 10111 10011 01001 11101 00001 10011 00001 00110 10010 11110 00101 00111 10000 01100 11011 10001 00001 01100 10000 11001 10110 00010 01101 00010".replace(' ', '')

# [Letters]WEATHER[Space]FORECAST[Space][Figures]HH:MM[Space]
# I changed it to
# [Letters]WEATHER[Space]FORECAST[Space][Figures]13:00[Space]
weather = "11111 11001 10000 11000 00001 00101 10000 01010 00100 10110 00011 01010 10000 01110 11000 10100 00001 00100 11011 11101 10000 01110 01101 01101 00100".replace(' ', '')


if __name__ == "__main__":

    # We Think that Weather and Msg_2 share the same opening.
    # If we XOR Weather and Msg_2 we should get part of the encryption Key used on the message.
    
    # Calculated by hand
    # decryption_key = '01111000110001001011100110011111111010001011001110101110011010101011101001001011110001011000010001111100010111001001100011001'

    # Programatic
    start_of_decryption_key = Utils.xor_binary(weather, msg_2[:len(weather)])


    #  Start with first 61 of decription key but reverse because of how LFSR works
    state = [int(digit) for digit in start_of_decryption_key[:61][::-1]]


    # Using Cache Owners Website https://html-preview.github.io/?url=https://github.com/mjcross/mod2MatrixTools/blob/master/mod2matrixtools.html
    # We use the Berlekamp-Massey algorithm to find the Taps for the LFSR
    poly = [1, 6, 7, 9, 10, 11, 13, 15, 16, 18, 20, 23, 27, 29, 30, 31, 42, 46, 48, 49, 50, 56, 58, 59, 60, 61]
    # The taps need to be highest to lowest, apparently, for the library.
    fpoly = poly[::-1]


    # #######################
    # Lets Decrupt all of Msg_2 By Generating the rest of the encryption Key.

    L = LFSR(fpoly=fpoly, initstate=state, verbose=False)
    tempseq = L.runKCycle(len(msg_2))
    key = "".join([str(x) for x in tempseq])

    y = Utils.xor_binary(key, msg_2)

    print(Utils.decode_baudot(y))
    print()

    # #######################
    # Msg_1 Was Generated directly before msg_2.
    # We need to run the lfsr in reverse to find out what the Encryption Key for the Previous Message was.

    key = Utils.lfsr_backwards(fpoly, len(msg_1), start_of_decryption_key[:61][::-1])

    y = Utils.xor_binary(key, msg_1)

    print(Utils.decode_baudot(y))
    print()

