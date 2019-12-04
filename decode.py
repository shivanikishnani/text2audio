message_so_far = ""
bit_blocks_received = []
unprocessed_bits = ""
SMALL_BLOCK_SIZE = 5


#process_sound_from_stream is the only function that should be used by other files
#every other function is just a helper for process_sound_from_stream

#takes in a sound and prints out the message translated so far

#this function is intended to be called in a loop each time a sound is received

#The input sound_to_bits should be a function that takes in a sound and returns the bits encoded
#in the sound. "sound" here refers to the sound data received during the predetermined time window.
#With WINDOWING=True, the assumption is that the number of encoded bits is equal to
#SMALL_BLOCK_SIZE * 3. With WINDOWING=False, sound_to_bits can return any number of bits.

def process_sound_from_stream(sound, sound_to_bits, WINDOWING=True):
    global bit_blocks_received
    global unprocessed_bits
    bit_blocks_received += sound_to_bits(sound)
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
        return "."
    if(n == 27):
        return " "
    return chr(n + 96)


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
