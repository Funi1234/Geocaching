# import LFSR
import numpy as np
from pylfsr import LFSR
import string

import random

# Encoding: ITA2, LSB last
letters_LSB_5 = {
        '00000': 'NULL', '00001': 'E', '00010': '\n', '00011': 'A', '00100': ' ', '00101': 'S', '00110': 'I',
        '00111': 'U', '01000': '\r', '01001': 'D', '01010': 'R', '01011': 'J', '01100': 'N', '01101': 'F',
        '01110': 'C', '01111': 'K', '10000': 'T', '10001': 'Z', '10010': 'L', '10011': 'W', '10100': 'H',
        '10101': 'Y', '10110': 'P', '10111': 'Q', '11000': 'O', '11001': 'B', '11010': 'G',
        '11100': 'M', '11101': 'X', '11110': 'V'
    }

figures_LSB_5 = {
        '00000': 'NULL', '00001': '3', '00010': '\n', '00011': '-', '00100': ' ', '00101': "'", '00110': '8',
        '00111': '7', '01000': '\r', '01001': '$', '01010': '4', '01011': '\'', '01100': ',', '01101': '!',
        '01110': ':', '01111': '(', '10000': '5', '10001': '"', '10010': ')', '10011': '2', '10100': '#',
        '10101': '6', '10110': '0', '10111': '1', '11000': '9', '11001': '?', '11010': '&', '11100': '.', '11101': '/', '11110': ';'
    }


# Encoding: ITA2, LSB first
letters_LSB_1 = {
    '00000': 'NULL', '10000': 'E', '01000': '\n', '11000': 'A', '00100': ' ', '10100': 'S', '01100': 'I', 
    '11100': 'U', '00010': '\r', '10010': 'D', '01010': 'R', '11010': 'J', '00110': 'N', '10110': 'F', 
    '01110': 'C', '11110': 'K', '00001': 'T', '10001': 'Z', '01001': 'L', '11001': 'W', '00101': 'H', 
    '10101': 'Y', '01101': 'P', '11101': 'Q', '00011': 'O', '10011': 'B', '01011': 'G', '00111': 'M', 
    '10111': 'X', '01111': 'V'}

figures_LSB_1 = {
    '00000': 'NULL', '10000': '3', '01000': '\n', '11000': '-', '00100': ' ', '10100': "'", '01100': '8', 
    '11100': '7', '00010': '\r', '10010': '$', '01010': '4', '11010': "'", '00110': ',', '10110': '!', 
    '01110': ':', '11110': '(', '00001': '5', '10001': '"', '01001': ')', '11001': '2', '00101': '#', 
    '10101': '6', '01101': '0', '11101': '1', '00011': '9', '10011': '?', '01011': '&', '00111': '.', '10111': '/', '01111': ';'
}



def decode_baudot(code):
    # Get rid of literal spaces
    code = code.replace(' ', '')

    letters = letters_LSB_1
    figures = figures_LSB_1

    current_map = letters  # Start with letters map
    decoded_text = ""

    length = 0

    for i in range(0, len(code), 5):
        length+=1
        current_char = code[i:i + 5]
        if current_char == '11111':  # Switch to letters
            current_map = letters
        elif current_char == '11011':  # Switch to figures
            current_map = figures
        else:
            decoded_text += current_map[current_char]

    # print(length)
    return decoded_text

def encode_baudot(msg):
    # To Encode we want the Key and Value to be swapped
    letters = {value: key for key, value in letters_LSB_1.items()}
    figures = {value: key for key, value in figures_LSB_1.items()}

    current_map = letters
    encoded_text = ""

    for c in msg:
        current_char = c.upper()
        if current_char not in current_map.keys():
            # Print a map change and then change flag
            if current_map == letters:
                encoded_text += "11011 "
                current_map = figures
            elif current_map == figures:
                encoded_text += "11111 "
                current_map = letters

        encoded_text += current_map[current_char]+" "

    return encoded_text

def xor_binary(bin_str1, bin_str2):
    if len(bin_str1) != len(bin_str2):
        raise ValueError("Binary strings must have the same length.")

    result = ""
    for bit1, bit2 in zip(bin_str1, bin_str2):
        if bit1 == '0' and bit2 == '0':
            result += '0'
        elif bit1 == '1' and bit2 == '1':
            result += '0'
        else:
            result += '1'
    return result


def lfsr_backwards(taps, lookback, init_state, value=''):
    """
    This function takes in part of a Key generated using an LFSR and runs it backwards `loopback` times. 
    """
    to_check = init_state[1:]+'1'
    state = [int(digit) for digit in to_check]

    L = LFSR(fpoly=taps, initstate=state, verbose=False)
    x = L.runKCycle(len(init_state)+1)

    if str(x[-1]) == str(init_state[0]):
        value = '1'+ value
        next_state = to_check
        # print('1', end='')
    else:
        value = '0'+ value
        next_state = init_state[1:]+'0'
        # print('0', end='')

    if len(value) >= lookback:
        print()
        return value
    else:
        return lfsr_backwards(taps, lookback,next_state,value)

        
       