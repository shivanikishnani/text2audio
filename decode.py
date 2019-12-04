message_so_far = ""
bit_blocks_received = []
unprocessed_bits = ""
SMALL_BLOCK_SIZE = 15


#process_sound_from_stream is the only function that should be used by other files
#every other function is a helper for process_sound_from_stream
#takes in a sound and prints out the message translated so far
def process_sound_from_stream(sound):
    global bit_blocks_received
    global unprocessed_bits
    bit_blocks_received += sound_to_bits(sound)
    if(len(bit_blocks_received) >= 3):
        block1 = bit_blocks_received[-3]
        block2 = bit_blocks_received[-2]
        block3 = bit_blocks_received[-1]
        unprocessed_bits += three_blocks_to_one(block1, block2, block3)
    
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


#takes sounds and turns it into one big block
def sound_to_bits(sound):
    #TODO
    return None


#takes in five bits and returns corresponding letter
def five_to_letter(bits):
    n = int(bin, 2)
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


