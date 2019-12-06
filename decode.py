message_so_far = ""
bit_blocks_received = []
unprocessed_bits = ""
SMALL_BLOCK_SIZE = 5
import math

#both receiver and sender should agree on F and k beforehand
#F is the total number of possible frequencies
#k is the number of frequencies we are sending
#permutation_into_num takes in an array of peaks loc_array and returns an integer
#num_into_permutation takes in an integer n and returns an array of peaks

def permutation_into_num(loc_array, F):
    total = 0
    for i in range(len(loc_array)):
        total += choose(F - loc_array[i] - 1, len(loc_array) - i)
    return total

def num_into_permutation(n, F, k):
    return num_into_permutation_helper(n + 1, F, k)

def num_into_permutation_helper(n, F, k):
    i = k
    if(k == 0):
        return []
    while(n > choose(i, k)):
        i+=1
    base_amount = choose(i - 1, k)
    return [F - i] + [x + (F - i + 1) for x in num_into_permutation_helper(n - base_amount, i - 1, k - 1)]

def choose(n, r):
    if(r > n):
        return 0
    fact = math.factorial
    return (fact(n))/(fact(r)*fact(n - r))

#process_sound_from_stream is the only function that should be used by other files
#every other function is just a helper for process_sound_from_stream

#takes in a sound and prints out the message translated so far

#this function is intended to be called in a loop each time a sound is received

#The input sound_to_bits should be a function that takes in sound_data and returns the bits encoded
#in the sound. "sound_data" here refers to the sound data received during the predetermined time window.
#With WINDOWING=True, the assumption is that the number of encoded bits is equal to
#SMALL_BLOCK_SIZE * 3. With WINDOWING=False, sound_to_bits can return any number of bits.

def process_sound_from_stream(sound_data, sound_to_bits, WINDOWING=True):
    global bit_blocks_received
    global unprocessed_bits
    bit_blocks_received += sound_to_bits(sound_data)
    if(WINDOWING):
        if(len(bit_blocks_received) >= 3):
            block1 = bit_blocks_received[-3]
            block2 = bit_blocks_received[-2]
            block3 = bit_blocks_received[-1]
            unprocessed_bits += three_blocks_to_one(block1, block2, block3)
    else:
        unprocessed_bits += bit_blocks_received[-1]
    
    while(len(unprocessed_bits) >= 5):
        process_five()

    print(message_so_far)


#takes the first five unprocessed bits, translates them, removes them from unprocessed_bits
#and adds the translated letter to the end of the message so far
def process_five():
    global unprocessed_bits
    global message_so_far

    first_five = unprocessed_bits[0:5]
    rest = unprocessed_bits[5:]

    message_so_far += five_to_letter(first_five)
    unprocessed_bits = rest


#takes in five bits and returns corresponding letter
def five_to_letter(bits):
    n = int(bits, 2)
    if(n == 28):
        return '.'
    if(n == 27):
        return ' '
    char = chr(n + 96)
    if(char in "abcdefghijklmnopqrstuvwxyz"):
        return char
    else:
        return '#'


#takes in three big blocks and returns one small block they all share
def three_blocks_to_one(block1, block2, block3):
    end_block1 = block1[SMALL_BLOCK_SIZE * 2:SMALL_BLOCK_SIZE * 3]
    mid_block2 = block2[SMALL_BLOCK_SIZE: SMALL_BLOCK_SIZE * 2]
    start_block3 = block3[0: SMALL_BLOCK_SIZE]
    
    new_small_block = ""
    for i in range(SMALL_BLOCK_SIZE):
        one_count = 0
        if(end_block1[i] == '1'):
            one_count += 1
        if(mid_block2[i] == '1'):
            one_count += 1
        if(start_block3[i] == '1'):
            one_count += 1
        
        if(one_count >= 2):
            new_small_block += '1'
        else:
            new_small_block += '0'
    
    return new_small_block


#test1:
#(make sure to set SMALL_BLOCK_SIZE=5 before running this test)
# a = "aaaaabbbbb01101"
# b = "aaaaa01101bbbbb"
# c = "01101aaaaabbbbb"
# print(three_blocks_to_one(a,b,c))

#expected_output:
# should print "01101" no matter how much you modify any one of the three strings.


#test2:
# unprocessed_bits = "11010baaaaaaaaaaaaaaaaaaaaaaa"
# process_five()
# print(message_so_far)
# print(unprocessed_bits)

#expected_output:
# should print the translation of 11010 aka 'z'
# then should print remaining unprocessed bits: "baaaaaaaaaaaaaaaaaaaaaaa"
